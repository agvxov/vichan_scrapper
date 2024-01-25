import getopt
#
import config
import usage

archive_all = False
integrity_check = False
only_integrity_check = False
is_service = False
restart_service = False

def opts(argv : list):
	global archive_all, integrity_check, only_integrity_check, is_service, restart_service
	try:
		opts = getopt.getopt(args = argv[1:], shortopts = 'ab:ish')[0]
		for o in opts:
			if o[0] == '-a':
				archive_all = True
				config.min_page = 1
				config.max_page = 10000
			elif o[0] == '-b':
				exec('config.boards = ' + o[1])
			elif o[0] == '-i':
				if not integrity_check:
					integrity_check = True
				else:
					only_integrity_check = True
			elif o[0] == '-s':
				if not is_service:
					is_service = True
				else:
					restart_service = True
			elif o[0] == '-h':
				usage.print_usage(argv[0])
				exit(0)
			else:
				raise getopt.GetoptError(msg = '', opt = o[0])
	except getopt.GetoptError as e:
		print("\033[31mUnrecognized command line option '{0}'.\033[0m".format(e.opt))
		usage.print_usage(argv[0])
		exit(1)
