import re
import nltk
from helpers.interfaces import *
from helpers.utils import AutoDict
from helpers.infogain import InformationGainMetric

import operator

class Splitter:

	pattern = re.compile('[.,;?!-_\r\n\t \'\"\\/\[\]*]')

class TrigramSplitter(Splitter):

	@staticmethod
	def split(data):

		data = Splitter.pattern.sub('', data.lower())

		current_word = ''
		for character in data:
			current_word = (current_word + character)[-3:]

			if len(current_word) < 3:
				continue

			yield current_word

class WordSplitter(Splitter):

	@staticmethod
	def split(data):

		data = Splitter.pattern.split(data.lower())
		data = filter(None, data)
		return data

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


class ElementsFrequencyCorpus(Corpus):

	VECTOR_MULTIPLIER = 1000

	def __init__(self, relevant, data_splitter):
		self.relevant = relevant
		self.data_splitter = data_splitter

	def __getstate__(self):
		return self.relevant, self.data_splitter

	def __setstate__(self, state):
		self.relevant, self.data_splitter = state

	def get_features_for_data(self, data):

		given = list(self.data_splitter.split(data))

		if len(given) > 0:

			given_frequency = AutoDict()
			for elem in given:
				given_frequency[elem] += 1

			features = [float(given_frequency[elem])/len(given)*self.VECTOR_MULTIPLIER for elem in self.relevant]

		else:
			features = [0 for elem in self.relevant]

		return features

class PartOfSpeechCorpus(Corpus):

	def init_freqs(self):

		self.unigram_freqs = AutoDict()
		self.bigram_freqs = AutoDict()

	def __init__(self, unigrams_most_common, bigrams_most_common):

		self.unigrams_most_common = unigrams_most_common
		self.bigrams_most_common = bigrams_most_common

		self.init_freqs()

	def __getstate__(self):

		return self.unigrams_most_common, self.bigrams_most_common

	def __setstate__(self, state):

		self.unigrams_most_common, self.bigrams_most_common = state

		self.init_freqs()

	def flatten_features(self, most_common, freqs):

		return [freqs[gram] for gram in most_common]

	def get_features_for_data(self, data):

		words = WordSplitter.split(data)
		poses = nltk.pos_tag(words)

		prev_pos = None

		for cur_pos in poses:
      # TODO exceptions? unknown word etc.
			self.unigram_freqs[cur_pos] += 1
			if prev_pos != None:
				self.bigram_freqs[(prev_pos, cur_pos)] += 1
			prev_pos = cur_pos

		unigram_features = self.flatten_features(self.unigrams_most_common, self.unigram_freqs)
		bigram_features = self.flatten_features(self.bigrams_most_common, self.bigram_freqs)

		return unigram_features + bigram_features


class PartOfSpeechCorpusCreator(CorpusCreator):

	MOST_COMMON_UNIGRAMS = 38
	MOST_COMMON_BIGRAMS = 1000

	def __init__(self):
		self.unigram_freqs = AutoDict()
		self.bigram_freqs = AutoDict()

	def feed_data(self, data, classification):

		words = WordSplitter.split(data)
		poses = nltk.pos_tag(words)

		prev_pos = None

		for cur_pos in poses:
      # TODO exceptions? unknown word etc.
			self.unigram_freqs[cur_pos] += 1
			if prev_pos != None:
				self.bigram_freqs[(prev_pos, cur_pos)] += 1
			prev_pos = cur_pos


	def create_corpus(self):

		unigrams_most_common = self.unigram_freqs

		minus_pair_right = lambda (x, y): -y
		bigrams_sorted = sorted(self.bigram_freqs.iteritems(), key=minus_pair_right)

		bigrams_most_common = map(operator.itemgetter(0), bigrams_sorted[:self.MOST_COMMON_BIGRAMS])
  
		return PartOfSpeechCorpus(unigrams_most_common, bigrams_most_common)

