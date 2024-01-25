import os
import multiprocessing
import hashlib
import sqlite3
import requests as req
from bs4 import BeautifulSoup
#
from antiRange import AntiRange, anti_ranges
import db
import config
import opts

def try_get(url : str):
	try:
		return req.get(url, timeout = config.request_time_out)
	except (req.exceptions.ConnectionError, req.exceptions.Timeout) as e:
		print('\033[31mConnection error on {0}\033[0m'.format(url), vars(e))
		return None

def print_status_got(page : int, status : int):
	print('\033[32mOn page {page}, got {color}\'{status}\'\033[32m.\033[0m'
			.format(page = page,
					color = '\033[32m' if status == 200 else '\033[33m',
					status = status
				)
		)

def get_threads_from_page(url : str):	
	response = try_get(url)
	if response == None:
		return
	threads = BeautifulSoup(
					response.text,
					'html.parser'
				) \
				.find_all(class_='thread')
	return response, threads

def get_boards_from_site():
	r = try_get(config.base_url)
	if r == None:
		return
	board_elements = BeautifulSoup(
						r.text,
						'html.parser'
					) \
					.find("select") \
					.find_all("option")
	boards = [db.Board(i['value'], i.text) for i in board_elements[2:]]
	return boards

def archive_op(bs : BeautifulSoup, board : str):
	op = bs.find(class_='op')
	no = op.find_all(class_='post_no')[1].text
	if db.is_post_archieved(board, int(no)):
		return no
	subject = op.find(class_='subject')
	subject = subject.text if subject != None else ''
	t = db.Post(
				no = no,
				poster = op.find(class_='name').text,
				poster_id = op.find(class_='poster_id').text,
				date = op.find('time').text,
				subject = subject,
				text = op.find(class_='body').decode_contents(),
				board = board,
				num_files = len(op.find_all(class_='file'))
			)
	db.insert_post(t, board)
	return no

def archive_posts(op : str, bs : BeautifulSoup, board : str):
	posts = bs.find_all(class_='reply')
	posts.reverse()
	for p in posts:
		no = p.find_all(class_='post_no')[1].text
		if db.is_post_archieved(board, int(no)):
			return
		post = db.Post(
					no = no,
					poster = p.find(class_='name').text,
					poster_id = p.find(class_='poster_id').text,
					date = p.find('time').text,
					text = p.find(class_='body').decode_contents(),
					thread = op,
					num_files = len(p.find_all(class_='file'))
				)
		db.insert_post(post, board)

def archive_file(board : str, post : str, fileinfo : BeautifulSoup, c : sqlite3.Connection, clutter = False):
		name = fileinfo.find('span')\
						.find('span').text
		path = 'files/' + hashlib.blake2s(name.encode()).hexdigest()
		if not clutter and os.path.isfile(path):
			print('\t\33[33mFile \033[34m\'', path, '\'\033[33m already exists.\033[0m', sep='')
			return
		r = try_get(config.base_url + fileinfo.find('a').attrs['href'])
		if r == None:
			return
		with open(path, 'wb') as f:
			f.write(r.content)
		f = db.File(
				name,
				post,
				board,
				path
		)
		db.insert_file(f, c)

def archive_files(bs : BeautifulSoup, board : str):
	multiprocessing.Event()
	files = bs.find(class_='files')
	for fileinfo in files.find_all(class_='fileinfo'):
		archive_file(board,
						bs.find(class_='thread').attrs['id'].split('_')[1],
						fileinfo,
						db.connection_pool[0]
					)
	thread_pool = []
	for p in bs.find_all(class_='post')[1:]:
		i = p.find_all(class_='fileinfo')
		for fileinfo in i:
			no = p.attrs['id'].split('_')[1]
			con = None
			while 1:
				with db.connection_pool_lock:
					if len(db.connection_pool) != 0:
						con = db.connection_pool.pop(0)
				if con == None:
					db.connection_produced.wait()
				else:
					break
			thread = multiprocessing.Process(target=archive_file, args=[board, no, fileinfo, con])
			with db.connection_pool_lock:
				db.connection_pool.append(con)
			thread.daemon = True
			thread_pool.append(thread)
			thread.start()
	for t in thread_pool:
		t.join()

def archive_thread(url : str, board : str):
	print(''.join(['\033[33mScrapping: ', url, '.\033[0m']))
	response = try_get(url)
	if response == None:
		return
	if response.url == config._404_url:
		print('\033[31mThread at ', url, ' 404d. It seems like it has been deleted in the meanwhile.\033[0m')
		return
	p = BeautifulSoup(
						response.text,
						'html.parser'
					)
	del response
	if not opts.archive_all and not config.is_thread_allegeable(p):
		return
	op = archive_op(p, board)
	archive_posts(op, p, board)
	archive_files(p, board)

def archive_threads(board_name : str, threads : list):
	# the magic number '7' is len('thread_')
	for t in threads:
		archive_thread(
						''.join([config.base_url, '/', board_name, '/res/', t.attrs['id'][7:], '.html']),
						board_name
					)


def archive_board(board_name : str):
	board_url = config.base_url + board_name
	status = 0
	for i in range(config.min_page, config.max_page):
		if i == 1:
			url = board_url + '/index.html'
		else:
			url = ''.join([board_url, '/', str(i), ".html"])
		try:
			response, threads = get_threads_from_page(url)
		except TypeError:
			continue
		print_status_got(i, response.status_code)
		if response.url == (config._404_url):
			return
		elif response.status_code != 200:	# add better error handling
			#talom['board_url'] = ['board', 5]
			continue
		archive_threads(board_name, threads)


def repair_corrupted(board : str, op : str, no : str):
	response = try_get(''.join([config.base_url, '/', board, '/res/', op, '.html']))
	if response == None:
		return
	thread = BeautifulSoup(
			response.text,
			'html.parser'
		)
	posts = thread.find_all(class_='post')
	fileinfos = None
	l = 0
	h = len(posts)-1
	while 1:
		c = int((l + h) / 2)
		n = posts[c].attrs['id'].split('_')[1]
		if n == no:
			fileinfos = posts[c].find_all(class_='fileinfo')
			break
		if h - l < 2:
			hno = posts[h].attrs['id'].split('_')[1]
			if hno == no:
				fileinfos = posts[h].find_all(class_='fileinfo')
			break
		if n < no:
			l = c
		else:
			h = c
	if fileinfos == None:
		print('\033[31mCould not fetch fileinfos for \033[34m(', board, ', ', no, ')\033[31m.\033[0m', sep='' )
		return
	thread_pool = []
	for fi in fileinfos:
		while 1:
			with db.connection_pool_lock:
				if len(db.connection_pool) != 0:
					con = db.connection_pool.pop(0)
			if con == None:
				db.connection_produced.wait()
			else:
				break
		thread = multiprocessing.Process(target=archive_file, args=[board, no, fi, con, True])
		with db.connection_pool_lock:
			db.connection_pool.append(con)
		thread.daemon = True
		thread_pool.append(thread)
		thread.start()
	for t in thread_pool:
		t.join()
	print('\033[32mRepaired: \033[34m', board, '/', no, '\033[32m.\033[0m', sep='')
