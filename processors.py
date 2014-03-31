
class Classification:

	def __init__(self, gender, age):
		self.gender = gender
		self.age = age


class Processor:
	""" Typically, only one of the methods record_char and record_word
	 will be non-empty, but both will be called on the corresponding events
	 (on char collected/on word complete)"""

	def record_char(self, c):
		"""Non-empty for e.g. CNG"""
		pass

	def record_word(self, w):
		"""Non-empty for e.g. FW, POS, CW"""
		pass


class CorpusProcessor(Processor):

	def switch_article(self, classification):
		"""Start collecting data for the new article
		relevant e.g. when IG is being computed, like for CW and CNG"""
		pass

	def get_corpus_wide_stats(self):
		"""The result can be even a simple list, dict or a tuple -
		 no need to return an instance of a specialized object"""
		pass


class ArticleProcessor(Processor):

	def set_corpus_wide_stats(self, stats):
		pass

	def clean_up(self):
		"""Used to clean up the stored state,
		just before the new article is started"""
		pass

	def get_features(self):
		"""Return a NEWLY CREATED flat list with features
		for the moment being - typically clean_up will be called after the call to get_features"""
		pass
