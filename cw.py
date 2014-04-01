
from processors import *
from math import log

class CWCorpusProcessor(CorpusProcessor):

	MOST_COMMON_TAKEN = 100
	HIGHEST_INFOGAINS_TAKEN = 10


	def __init__(self):

		self.currect_art_category = 0
		self.current_art_word_set = set()

		self.freq_entries_by_word = {}
		self.freqs_by_category = self.new_freq_entry()


	def switch_article(self, clsfn):
		"""The classification is represented by a Classification object"""

		self.currect_art_category = clsfn.get_category_number()
		self.current_art_word_set = set()

		self.freqs_by_category[self.currect_art_category] += 1


	def first_occurred_in_current_article(self, w):

		return w not in self.current_art_word_set

	def new_freq_entry(self):

		return [0] * Classification.NUMBER_OF_CATEGORIES

	def freq_entry_total(self, freq_entry):

		return sum(freq_entry)

	def freq_entry_female(self, freq_entry):

		return sum(freq_entry[:4])

	def freq_entry_male(self, freq_entry):

		return sum(freq_entry[4:])

	def record_word(self, w):

		if self.first_occurred_in_current_article(w):

			self.current_art_word_set.add(w)

			freq_entry = self.freq_entries_by_word.get(w)

			if not freq_entry:
				freq_entry = self.freq_entries_by_word[w] = self.new_freq_entry()

			freq_entry[self.currect_art_category] += 1


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

		# just not to miss the minus
		get_minus_freq = lambda (word, freq_entry): ((((-1)))) * self.freq_entry_total(freq_entry)

		word_freq_list = self.freq_entries_by_word.items()
		sorted_by_freq_desc = sorted(word_freq_list, key=get_minus_freq)

		return sorted_by_freq_desc[:self.MOST_COMMON_TAKEN]


	def get_highest_ig(self, words_most_common):

		infogains = []

		for (word, freq_entry) in words_most_common:
			print word, self.freq_entry_female(freq_entry), self.freq_entry_male(freq_entry)
			ig = self.get_infogain(freq_entry)
			infogains.append((word, ig))

		get_minus_ig = lambda (word, ig): -ig
		infogains.sort(key=get_minus_ig)

		print infogains

		words_highest_ig = [word for (word, ig) in infogains[:self.HIGHEST_INFOGAINS_TAKEN]]
		return words_highest_ig

	def get_infogain(self, freq_entry):

		log2_or_zero = lambda x: log(x, 2) if x else 0.0
		div_or_zero = lambda m, n: (float(m) / n) if n else 0.0

		# computed according to http://www.cise.ufl.edu/~ddd/cap6635/Fall-97/Short-papers/2.htm
		total_containing = self.freq_entry_total(freq_entry)
		female_containing = self.freq_entry_female(freq_entry)
		male_containing = self.freq_entry_male(freq_entry)
		f = div_or_zero(female_containing, total_containing)
		m = div_or_zero(male_containing, total_containing)
		print total_containing, female_containing, male_containing, f, m

		total = self.freq_entry_total(self.freqs_by_category)
		total_female = self.freq_entry_female(self.freqs_by_category)
		total_male = self.freq_entry_male(self.freqs_by_category)

		total_not_containing = total - total_containing
		female_not_containing = total_female - female_containing
		male_not_containing = total_male - male_containing
		nf = div_or_zero(female_not_containing, total_not_containing)
		nm = div_or_zero(male_not_containing, total_not_containing)
		print total_not_containing, female_not_containing, male_not_containing, nf, nm

		entropy_word_present = - m * log2_or_zero(m) - f * log2_or_zero(f)
		entropy_word_absent = - nm * log2_or_zero(nm) - nf * log2_or_zero(nf)

		# use div_or_zero in the case corpus is empty (self.total_number() == 0)
		prop_word_present = div_or_zero(total_containing, total)
		prop_word_absent = div_or_zero(total_not_containing, total)

		# it's not really the infogain,
		# since the formula also incorporates the part for entropy H(S) -
		# this can be safely skipped, however
		ig = - prop_word_present * entropy_word_present - prop_word_absent * entropy_word_absent
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
