
from processors import *
from math import log

class CWCorpusProcessor(CorpusProcessor):

	MOST_COMMON_TAKEN = 10000
	HIGHEST_INFOGAINS_TAKEN = 1000


	def __init__(self):

		self.current_art_category = 0
		self.current_art_word_set = set()

		self.arts_by_categories_by_word = {}
		self.arts_by_category = self.new_arts_by_category_array()


	def switch_article(self, clsfn):
		"""The classification is represented by a Classification object"""

		self.current_art_category = clsfn.get_category_number()
		self.current_art_word_set = set()

		self.arts_by_category[self.current_art_category] += 1


	def first_occurred_in_current_art(self, w):

		return w not in self.current_art_word_set


	def new_arts_by_category_array(self):

		return [0] * Classification.NUMBER_OF_CATEGORIES



	def record_word(self, w):

		if self.first_occurred_in_current_art(w):

			self.current_art_word_set.add(w)

			arts_by_categories_for_the_word = self.arts_by_categories_by_word.get(w)

			if not arts_by_categories_for_the_word:
				arts_by_categories_for_the_word = self.arts_by_categories_by_word[w] = self.new_arts_by_category_array()

			arts_by_categories_for_the_word[self.current_art_category] += 1


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
		get_minus_total_freq = lambda (word, arts_by_categories_for_the_word): \
			((((-1)))) * sum(arts_by_categories_for_the_word)

		word_entry_list = self.arts_by_categories_by_word.items()
		sorted_by_freq_desc = sorted(word_entry_list, key=get_minus_total_freq)

		return sorted_by_freq_desc[:self.MOST_COMMON_TAKEN]


	def get_highest_ig(self, words_most_common):

		infogains = []

		for (word, arts_by_categories_for_the_word) in words_most_common:
			print word, arts_by_categories_for_the_word
			ig = self.get_infogain(arts_by_categories_for_the_word)
			infogains.append((word, ig))

		get_minus_ig = lambda (word, ig): -ig
		infogains.sort(key=get_minus_ig)

		print infogains

		words_highest_ig = [word for (word, ig) in infogains[:self.HIGHEST_INFOGAINS_TAKEN]]
		return words_highest_ig


	def get_infogain(self, arts_by_categories_for_the_word):

		log2_or_zero = lambda x: log(x, 2) if x else 0.0
		div_or_zero = lambda m, n: (float(m) / n) if n else 0.0

		total = sum(self.arts_by_category)
		total_containing_the_word = sum(arts_by_categories_for_the_word) # sum over categories
		total_not_containing_the_word = total - total_containing_the_word

		entropy_in_arts_containing_the_word = 0.0
		for i in range(len(arts_by_categories_for_the_word)):
			in_category_containing = arts_by_categories_for_the_word[i]
			prop_containing_is_in_category = div_or_zero(in_category_containing, total_containing_the_word)
			entropy_in_arts_containing_the_word += (((-1))) * prop_containing_is_in_category \
												   * log2_or_zero(prop_containing_is_in_category)

		prop_art_contains_the_word = div_or_zero(total_containing_the_word, total)


		entropy_in_arts_not_containing_the_word = 0.0
		for i in range(len(arts_by_categories_for_the_word)):
			in_category_not_containing = self.arts_by_category[i] - arts_by_categories_for_the_word[i]
			prop_not_containing_is_in_category = div_or_zero(in_category_not_containing, total_not_containing_the_word)
			entropy_in_arts_not_containing_the_word += (((-1))) * prop_not_containing_is_in_category \
													   * log2_or_zero(prop_not_containing_is_in_category)

		prop_art_doesnt_contain_the_word = div_or_zero(total_not_containing_the_word, total)


		print prop_art_contains_the_word, entropy_in_arts_containing_the_word, \
			prop_art_doesnt_contain_the_word, entropy_in_arts_not_containing_the_word
		ig = - prop_art_contains_the_word * entropy_in_arts_containing_the_word \
			 - prop_art_doesnt_contain_the_word * entropy_in_arts_not_containing_the_word
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
