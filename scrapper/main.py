#!/bin/python3
import os
import sys
import fcntl
import signal
import multiprocessing
from bs4 import BeautifulSoup
#
from antiRange import AntiRange, anti_ranges
import scrap
import db
import opts
import config

#talom = {}
lockf = None

def handler(signum, frame):
	print('\033[31mReceived SIGINT, exiting...\033[0m')
	exit(1)

def main(argv):
	signal.signal(signal.SIGINT, handler)
	# ---
	opts.opts(argv)
	# ---
	db.connections_init()
	# ---
	if opts.is_service:
		lockpath = 'service/scrapper.lock'
		lockf = open(lockpath, 'r+')
		while 1:
			try:
				fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
				break
			except OSError:
				if opts.restart_service:
					prev_inst_pid = int(lockf.read())
					os.kill(prev_inst_pid, signal.SIGINT)
					print('\033[31mPrevious instance (\033[34m', prev_inst_pid, '\033[31m) killed.\033[0m', sep='')
					import time
					time.sleep(1)
				else:
					print('\033[31mAnother instance is blocking execution. Quiting...\033[0m')
					signal.raise_signal(signal.SIGINT)
					# NOT REACHED
		pid = os.getpid()
		lockf.seek(0, 0)
		lockf.truncate()
		lockf.write(str(pid))
		lockf.flush()
	# ---
	if opts.integrity_check:
		corrupted = db.corrupt_posts()
		print('\033[31mFound the following threads to be corrupted: \033[34m', str(corrupted), '\033[31m.\033[0m', sep='')
		for c in corrupted:
			board = c[0]
			no = str(c[1])
			op = str(c[2])
			got = 0 if c[3] == None else str(c[3])
			expected = c[4]
			print('\033[33mRepairing: \033[34m', board, no, ' (', got, '/', expected, ')\033[33m.\033[0m', sep='')
			scrap.repair_corrupted(board, op, no)
		if opts.only_integrity_check:
			return 0
	# ---
	if config.boards == []:
		print('\033[33mScrapping board names... \033[0m', end='')
		boards = scrap.get_boards_from_site()
		if boards == None:
			signal.raise_signal(signal.SIGINT)
		print('\033[32mDone. Got:\033[0m', '\033[34m{0}\033[0m'.format(str([b.name for b in boards])))
	else:
		boards = config.boards
	# ---
	for b in boards:
		print('\033[33mArchiving board: \033[34m\'{0}\'\033[0m'.format(b.name))
		db.insert_board(b)
		anti_ranges[b.name] = db.board2antirange(b.name)
		scrap.archive_board(b.name)
		print('\033[32mArchived board: \033[34m\'{0}\'\033[0m'.format(b.name))
	# ---
	print('\033[32mFinished.')
			

if __name__ != '__main__': 
	exit(1)

main(sys.argv)
