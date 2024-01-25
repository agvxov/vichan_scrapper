usage_msg = '''\033[1m{0} [options]\033[0m
	-a        : scrap all; ignore all filters
	-b <list> : provide a list of boards to archive
	             the default is all that can be found
	             <list> must be a valid python list of strings
	-i        : perform integrity check; specify twice to do not carry on with regular scrapping
	'''

def print_usage(program_name = 'scrapper'):
	print(usage_msg.format(program_name))
