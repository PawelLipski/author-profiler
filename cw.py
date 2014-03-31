
from processors import *

class CWCorpusProcessor(CorpusProcessor):

	MOST_COMMON_TAKEN = 100
	HIGHEST_INFOGAIN_TAKEN = 10

	def __init__(self):
		self.freqs = {}

	def record_word(self, w):

		if w in self.freqs:
			self.freqs[w] += 1
		else:
			self.freqs[w] = 1

	def switch_article(self, classification):
		"""The classification is represented by a pair
		of gender's first letter and age lower bound
		('F' or 'M', 18 or 25 or 35 or 50)"""

		gender, age = classification
		self.is_current_by_male = gender == 'M'

	def get_corpus_wide_stats(self):
		"""Returns the list of 1k words with the highest IG
		among the 10k most common words.
		The corresponding ArticleProcessor must accept such a list of 1k words
		as the param to set_corpus_wide_stats."""

		words_most_common = self.get_most_common()
		print words_most_common
		words_highest_ig = self.get_highest_ig(words_most_common)

		return words_highest_ig

	def get_most_common(self):

		get_minus_freq = lambda (word, freq): -freq

		word_freq_list = self.freqs.items()
		sorted_by_freq_desc = sorted(word_freq_list, key = get_minus_freq)

		return sorted_by_freq_desc[:self.MOST_COMMON_TAKEN]

	def get_highest_ig(self, words_most_common):

		infogains = []

		for w in words_most_common:
			ig_w = self.get_infogain(w)
			infogains.append((w, ig_w))

		# TODO
		return words_most_common[:self.HIGHEST_INFOGAIN_TAKEN]

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
