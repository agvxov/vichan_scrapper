from bs4 import BeautifulSoup

# Logical function to determine wheter a thread should be archived.
#  On return:
#    True  - do archive
#    False - do not archive
#  All threads are filtered through this function unless '-a' is specified
def is_thread_allegeable(p : BeautifulSoup):
	return True

# Range of pages to designate for scrapping.
#  Ignored if '-a' is specified.
min_page = 1
max_page = 10000 # over shooting this value does not cause overhead
if min_page > max_page:
	raise Exception('Invalid page range [{0};{1}].'.format(min_page, max_page))

# List of boards to archive.
#  Overriden by '-b'.
#  Empty means 'all'.
boards = []

# Seconds to wait before giving up on each request
request_time_out = 5

# Domain to scrap from
base_url = 'https://examplechan.org'

# URL marking the 404 page
#  Dobiously it does not return a 404 response code, therefor the url must be tested.
_404_url = base_url + '/404.html'

# Maximum number of threads to create.
#  Should be 2-4 times the number of available CPU cores.
#  To determine the perfect value experimenting is recommended.
#  Go with <cores>*2 if you're clueless.
max_threads = 4
