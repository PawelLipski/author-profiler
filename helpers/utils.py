
class AutoDict(dict):
	def __init__(self, initializer = 0):
		super(dict, self).__init__()
		self.initializer = initializer
	
	def __getitem__(self, item):
		try:
			return dict.__getitem__(self, item)
		except KeyError:
			if callable(self.initializer):
				self[item] = self.initializer()
			else:
				self[item] = self.initializer
			
			return dict.__getitem__(self, item) 

