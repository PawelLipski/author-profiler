
from helpers.utils import AutoDict
from helpers.infogain import InformationGainMetric
from helpers.pos import PartOfSpeechTagger
from textprocess.splitters import *
from impl import *

import operator


class HighestInfogainCorpusCreator(CorpusCreator):

	MOST_COMMON_TAKEN = 10000
 	HIGHEST_INFOGAINS_TAKEN = 1000

	def __init__(self, data_splitter):

		self.elems_frequency = AutoDict()
		self.elems_classification = AutoDict(AutoDict)
		self.articles_classification = AutoDict()

		self.data_splitter = data_splitter

	def feed_data(self, data, classification):

		article_elems_list = list(self.data_splitter.split(data))
		article_elems_set = set(article_elems_list)

		for elem in article_elems_list:
			self.elems_frequency[elem] += 1

		self.articles_classification[classification.to_int()] += 1
		for elem in article_elems_set:
			self.elems_classification[elem][classification.to_int()] += 1

	def create_corpus(self):

		minus_pair_right = lambda (x, y): -y

		elems_freq_sorted = sorted(self.elems_frequency.iteritems(), key=minus_pair_right)

		elems_infogain = [
			(x[0], InformationGainMetric.get_infogain(self.articles_classification, self.elems_classification[x[0]]))
				for x in elems_freq_sorted[0:self.MOST_COMMON_TAKEN]
		]

		elems_infogain = sorted(elems_infogain, key=minus_pair_right)

		chosen_elems = [x[0] for x in elems_infogain[0:self.HIGHEST_INFOGAINS_TAKEN]]

		return ElementsFrequencyCorpus(chosen_elems, self.data_splitter)


class HighestInfogainTrigramsCorpusCreator(HighestInfogainCorpusCreator):

	def __init__(self):
		HighestInfogainCorpusCreator.__init__(self, TrigramSplitter())


class HighestInfogainWordsCorpusCreator(HighestInfogainCorpusCreator):

	def __init__(self):
		HighestInfogainCorpusCreator.__init__(self, WordSplitter())



class PartOfSpeechCorpusCreator(CorpusCreator):

	MOST_COMMON_BIGRAMS = 1000

	def __init__(self):
		self.unigram_freqs = AutoDict()
		self.bigram_freqs = AutoDict()

	def feed_data(self, data, classification):

		poses, pos_pairs = PartOfSpeechTagger.pos_ngrams_for_chunk(data)

		for pos in poses:
			self.unigram_freqs[pos] += 1

		for pos_pair in pos_pairs:
			self.bigram_freqs[pos_pair] += 1


	def create_corpus(self):

		unigrams_most_common = self.unigram_freqs

		minus_pair_right = lambda (x, y): -y
		bigrams_sorted = sorted(self.bigram_freqs.iteritems(), key=minus_pair_right)

		bigrams_most_common = map(operator.itemgetter(0), bigrams_sorted[:self.MOST_COMMON_BIGRAMS])
  
		return PartOfSpeechCorpus(unigrams_most_common, bigrams_most_common)


class FunctionWordsCorpusCreator(CorpusCreator):

	FUNCTION_WORDS_FILE = 'fws.txt'

	def __init__(self):
		pass

	def feed_data(self, data, classification):
		pass

	def create_corpus(self):

		function_words = [l.rstrip() for l in open(self.FUNCTION_WORDS_FILE).readlines()]

		return ElementsFrequencyCorpus(function_words, WordSplitter())

