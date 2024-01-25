# Constantly querying wheter we already have a post is expensive,
#  so is storing every post number in memory.
# Since we know that the posts we have is going to be mostly continuous (in production atleast)
#  we can store only the border values and the missing values in their range.
class AntiRange:
	def __init__(self, range_ : list):
		if range_ == []:
			import sys
			self.min_ = sys.maxsize
			self.max_ = 0
			self.not_ = []
			return
		self.min_ = min(range_)
		self.max_ = max(range_)
		self.not_ = list(set(range(self.min_, self.max_)) - set(range_))

anti_ranges = {}
