import sqlite3
import bisect
import multiprocessing
import random
import time
#
import config
from antiRange import AntiRange, anti_ranges

# --- Tricks i could still implement to make this faster ---
#		> connection pool
#		> pragma journal_mode = WAL;
#		> pragma synchronous = normal;

CONNECT_TO = "data.sqlite"

connection_pool = []
connection_pool_lock = multiprocessing.Lock()
connection_produced = multiprocessing.Event()

def connections_init():
	for i in range(config.max_threads):
		connection = sqlite3.Connection(CONNECT_TO, check_same_thread=False)
		connection_pool.append(connection)


class Board:
	def __init__(self, n, d):
		self.name = n
		self.description = d

class Post:
	def __init__(self, no, poster, date, text,
					poster_id = None,
					num_files = 0,
					subject = None,
					board = None,
					thread = None
				):
		if board == None and thread == None:
			raise Exception('Orphan post')
		self.no = no
		self.poster = poster
		self.date = date
		self.poster_id = poster_id
		self.num_files = num_files
		self.subject = subject
		self.text = text
		self.board = board
		self.thread = thread

class File:
	def __init__(self, name, post, board, path):
		self.name = name
		self.post = post
		self.board = board
		self.path = path

def corrupt_posts():
	with sqlite3.Connection(CONNECT_TO) as con:
		cursor = con.cursor()
		cursor.execute(
				'SELECT posts.board, posts.id, posts.thread, file_count.count, posts.num_files \
					FROM \
						posts \
					INNER JOIN \
							(SELECT post, board, count(*) AS count \
								FROM \
									files \
								GROUP BY post) \
						file_count ON \
							posts.id = file_count.post \
								AND \
							posts.board = file_count.board \
					WHERE \
						(file_count.count is null and posts.num_files != 0) \
							OR \
						file_count.count < posts.num_files \
					;'
		)
		return cursor.fetchall()

def is_post_archieved(board: str, no : int):
	ar = anti_ranges[board]
	if no > ar.max_ or  no < ar.min_:
		return False
	pos = bisect.bisect_left(ar.not_, no)
	if pos < len(ar.not_) and ar.not_[pos] == no:
		return False
	return True

def insert_file(f : File, con : sqlite3.Connection):
	query = "INSERT INTO files \
					(name, post, board, path) \
						VALUES \
					('{0}', '{1}', '{2}', '{3}');".format(
						f.name.replace("'", "''"),
						f.post,
						f.board,
						f.path
					)
	while 1:
		try:
			con.execute(query)
			con.commit()
			print('\t\033[32mArchived file \033[34m\"{0}\"\033[32m.\033[0m'.format(f.name))
			break
		except sqlite3.OperationalError:
			print('fuck, race condition', multiprocessing.current_process().pid)
			time.sleep(random.uniform(0.1, 1.0))

def insert_post(p : Post, board : str):
	if p.thread == None:
		var_col = 'subject'
		var_val = p.subject.replace("'", "''")
	else:
		var_col = 'thread'
		var_val = p.thread
	query = "INSERT INTO posts \
					( \
						id, \
						board, \
						name, \
						capcode, \
						time, \
						body, \
						num_files, \
						{var_col} \
					) \
						VALUES \
					( \
						'{id}', \
						'{board}', \
						'{name}', \
						'{capcode}', \
						'{date}', \
						'{body}', \
						{num_files}, \
						'{var_val}' \
					);".format(
						id = p.no,
						board = board,
						name = p.poster.replace("'", "''"),
						capcode = p.poster_id,
						date = p.date,
						body = p.text.replace("'", "''"),
						num_files = p.num_files,
						#
						var_col = var_col,
						var_val = var_val
					)
	try:
		with sqlite3.Connection(CONNECT_TO) as con:
			con.execute(query)
			msg = ''.join(['\t\033[32mArchived post no. \033[34m', p.no, '\033[32m'])
			if p.thread != None:
				msg = ''.join([msg, ' (belonging to thread: ', '\033[34m', p.thread, '\033[32m)'])
			msg = ''.join([msg, '.\033[0m'])
			print(msg)
	except sqlite3.IntegrityError:
		pass

def board2antirange(board : str):
	with sqlite3.Connection(CONNECT_TO) as con:
		query = "SELECT id FROM posts WHERE board = '{0}';".format(board)
		r = con.execute(query)
		return AntiRange([x[0] for x in r.fetchall()])
	

def insert_board(b : Board):
	try:
		with sqlite3.Connection(CONNECT_TO) as con:
			con.execute("INSERT INTO boards (name, desc) \
									VALUES \
								('{0}', '{1}');".format(
									b.name,
									b.description
								)
						)
	except sqlite3.IntegrityError:
		pass


