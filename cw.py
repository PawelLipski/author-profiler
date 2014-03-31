
from processors import *

class CWCorpusProcessor(CorpusProcessor):

	def __init__(self):
		self.freqs = {}

	def record_word(self, w):

		if w in self.freqs:
			self.freqs[w] += 1
		else:
			self.freqs[w] = 1

	def switch_article(self, classification):
		pass

	def get_corpus_wide_stats(self):
		"""Returns the list of 1k words with the highest IG
		among the 10k most common words.
		The corresponding ArticleProcessor must accept such a list of 1k words
		as the param to set_corpus_wide_stats."""

		words_10k = self.get_10k_most_common()
		words_1k_ig = self.get_1k_highest_ig(words_10k)

		return words_1k_ig

	def get_10k_most_common(self):

		# TODO
		return []

	def get_1k_highest_ig(self, words_10k):

		infogains = []

		for w in words_10k:
			ig_w = self.get_infogain(w)
			infogains.append((w, ig_w))

		# TODO
		return []

	def get_infogain(self, w):
		# TODO
		return 0.0



class CWArticleProcessor(ArticleProcessor):

	def set_corpus_wide_stats(self, words_1k_ig):
		"""Assumes stats is a list of 1k strings."""

		self.word_number = len(words_1k_ig)
		self.word_dict = {}

		for (no, w) in enumerate(words_1k_ig):
			self.word_dict[w] = (w, no)

		self.set_up_new_word_counts()

	def record_word(self, word):

		no = self.word_dict.get(word)
		if no:
			self.word_counts[no] += 1

	def get_features(self):

		return list(self.word_counts)

	def clean_up(self):

		self.set_up_new_word_counts()


	def set_up_new_word_counts(self):

		self.word_counts = [ 0 ] * self.word_number
