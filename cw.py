
from processors import *
from math import log

class WordFreqEntry:
	def __init__(self):
		self.male_containing = 0
		self.female_containing = 0

	def get_total_containing(self):
		return self.female_containing + self.male_containing


class CWCorpusProcessor(CorpusProcessor):

	MOST_COMMON_TAKEN = 100
	HIGHEST_INFOGAINS_TAKEN = 10


	def __init__(self):

		self.clsfn = None
		self.word_set = set()

		self.freqs = {}

		self.male_number = 0
		self.female_number = 0


	def get_total_number(self):
		return self.male_number + self.female_number


	def switch_article(self, clsfn):
		"""The classification is represented by a pair
		of gender's first letter and age lower bound
		('F' or 'M', 18 or 25 or 35 or 50)"""

		self.clsfn = clsfn
		if clsfn.gender == 'M':
			self.male_number += 1
		else:
			self.female_number += 1

		self.word_set = set()

	def first_occurred_in_current_article(self, w):

		return w not in self.word_set

	def record_word(self, w):

		if self.first_occurred_in_current_article(w):

			self.word_set.add(w)

			freq_entry = self.freqs.get(w)

			if not freq_entry:
				freq_entry = self.freqs[w] = WordFreqEntry()

			if self.clsfn.gender == 'M':
				freq_entry.male_containing += 1
			else:
				freq_entry.female_containing += 1


	def get_corpus_wide_stats(self):
		"""Returns the list of 1k words with the highest IG
		among the 10k most common words.
		The corresponding ArticleProcessor must accept such a list of 1k words
		as the param to set_corpus_wide_stats."""

		words_most_common = self.get_most_common()
		words_highest_ig = self.get_highest_ig(words_most_common)
		print words_highest_ig

		return words_highest_ig


	def get_most_common(self):

		get_minus_freq = lambda (word, freq): -freq.get_total_containing()

		word_freq_list = self.freqs.items()
		sorted_by_freq_desc = sorted(word_freq_list, key=get_minus_freq)

		return sorted_by_freq_desc[:self.MOST_COMMON_TAKEN]


	def get_highest_ig(self, words_most_common):

		infogains = []

		for (word, freq_entry) in words_most_common:
			print word, freq_entry.male_containing, freq_entry.female_containing
			ig = self.get_infogain(freq_entry)
			infogains.append((word, ig))

		get_minus_ig = lambda (word, ig): -ig
		infogains.sort(key=get_minus_ig)

		print infogains[:self.HIGHEST_INFOGAINS_TAKEN]

		words_highest_ig = [word for (word, ig) in infogains[:self.HIGHEST_INFOGAINS_TAKEN]]
		return words_highest_ig

	def div_or_zero(self, part, total):
		if total == 0:
			return 0.0
		else:
			return float(part) / total

	def get_infogain(self, freq_entry):

		log2_or_zero = lambda x: log(x, 2) if x else 0.0

		total_containing = freq_entry.get_total_containing()
		male_containing = freq_entry.male_containing
		female_containing = freq_entry.female_containing
		m = self.div_or_zero(male_containing, total_containing)
		f = self.div_or_zero(female_containing, total_containing)
		print total_containing, male_containing, female_containing, m, f

		total_not_containing = self.get_total_number() - total_containing
		male_not_containing = self.male_number - male_containing
		female_not_containing = self.female_number - female_containing
		nm = self.div_or_zero(male_not_containing, total_not_containing)
		nf = self.div_or_zero(female_not_containing, total_not_containing)
		print total_not_containing, male_not_containing, female_not_containing, nm, nf

		entropy_word_present = m * log2_or_zero(m) + f * log2_or_zero(f)
		entropy_word_absent = nm * log2_or_zero(nm) + nf * log2_or_zero(nf)

		p_c = total_containing / self.get_total_number()
		p_nc = total_not_containing / self.get_total_number()

		# it's not really the infogain,
		# since the formula also incorporates the part for entropy H(S) -
		# this can be safely skipped, however
		ig = - p_c * entropy_word_present - p_nc * entropy_word_absent
		return ig


class CWArticleProcessor(ArticleProcessor):
	def set_corpus_wide_stats(self, relevant_words):
		"""Assumes stats is a list of 1k strings."""

		self.word_number = len(relevant_words)
		self.relevant_words_dict = {}

		for (no, w) in enumerate(relevant_words):
			self.relevant_words_dict[w] = no

		self.set_up_new_word_counts()

	def record_word(self, word):

		no = self.relevant_words_dict.get(word)
		if no:
			self.word_counts[no] += 1

	def get_features(self):

		return list(self.word_counts)

	def clean_up(self):

		self.set_up_new_word_counts()


	def set_up_new_word_counts(self):

		self.word_counts = [0] * self.word_number
