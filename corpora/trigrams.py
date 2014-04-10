from helpers.interfaces import *
from helpers.utils import AutoDict
from helpers.infogain import InformationGainMetric
from textprocess.normalize import TextNormalizerProcessor

import operator

class TrigramsCorpusCreator(CorpusCreator):
	MOST_COMMON_TAKEN = 10000
	HIGHEST_INFOGAINS_TAKEN = 1000
	
	def __init__(self):
		self.trigrams_frequency = AutoDict()
		self.trigrams_classification = AutoDict(AutoDict)
		self.articles_classification = AutoDict()
	
	def feed_data(self, data, classification):
		data = TextNormalizerProcessor.process(data)
		
		article_trigrams = dict()
		
		current_word = ''
		for character in data:
			current_word = (current_word + character)[-3:]
			
			if len(current_word) < 3:
				continue
			
			article_trigrams[current_word] = 1
			self.trigrams_frequency[current_word] += 1
		
		self.articles_classification[classification.to_int()] += 1
		for trigram in article_trigrams:
			self.trigrams_classification[trigram][classification.to_int()] += 1
	
	def create_corpus(self):
		trigrams_freq_sorted = sorted(self.trigrams_frequency.iteritems(), key=operator.itemgetter(1))
		trigrams_infogain = [
			(x[0], InformationGainMetric.get_infogain(self.articles_classification, self.trigrams_classification[x[0]]))
				for x in trigrams_freq_sorted[0:self.MOST_COMMON_TAKEN]
		]
		
		trigrams_infogain = sorted(trigrams_infogain, key=operator.itemgetter(1))
		
		return TrigramsCorpus([x[0] for x in trigrams_infogain[0:self.HIGHEST_INFOGAINS_TAKEN]])

class TrigramsCorpus(Corpus):
	VECTOR_MULTIPLIER = 1000
	
	def __init__(self, trigrams = []):
		self.trigrams = trigrams
	
	def __getstate__(self):
		return self.trigrams
	
	def __setstate__(self, state):
		self.trigrams = state
	
	def get_features_for_data(self, data):
		data = TextNormalizerProcessor.process(data)
		if len(data) >= 3:
			trigrams_number = len(data)-2
			features = [float(data.count(trigram))/trigrams_number*self.VECTOR_MULTIPLIER for trigram in self.trigrams]
		else:
			features = [0 for trigram in self.trigrams]
		return features


class TrigramSplitter:

	@staticmethod
	def split(data):

		current_word = ''
		for character in data:
			current_word = (current_word + character)[-3:]

			if len(current_word) < 3:
				continue

			yield current_word


class HighestInfogainCorpusCreator(CorpusCreator):

	MOST_COMMON_TAKEN = 10000
	HIGHEST_INFOGAINS_TAKEN = 1000

	def __init__(self):

		print 'instantiate HighestInfogainCorpusCreator'

		self.elems_frequency = AutoDict()
		self.elems_classification = AutoDict(AutoDict)
		self.articles_classification = AutoDict()

		self.data_splitter = TrigramSplitter

	def feed_data(self, data, classification):

		data = TextNormalizerProcessor.process(data)

		article_elems_list = list(self.data_splitter.split(data))
		article_elems_set = set(article_elems_list)

		for elem in article_elems_list:
			self.elems_frequency[elem] += 1

		self.articles_classification[classification.to_int()] += 1
		for elem in article_elems_set:
			self.elems_classification[elem][classification.to_int()] += 1

	def create_corpus(self):
		elems_freq_sorted = sorted(self.elems_frequency.iteritems(), key=operator.itemgetter(1))

		elems_infogain = [
			(x[0], InformationGainMetric.get_infogain(self.articles_classification, self.elems_classification[x[0]]))
				for x in elems_freq_sorted[0:self.MOST_COMMON_TAKEN]
		]

		elems_infogain = sorted(elems_infogain, key=operator.itemgetter(1))

		elems_infogain = [x[0] for x in elems_infogain[0:self.HIGHEST_INFOGAINS_TAKEN]]

		return ElementsFrequencyCorpus(elems_infogain, TrigramSplitter())


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

		data = TextNormalizerProcessor.process(data)
		given = list(self.data_splitter.split(data))

		if len(given) > 0:

			given_frequency = AutoDict()
			for elem in given:
				given_frequency[elem] += 1

			features = [float(given_frequency[elem])/len(given)*self.VECTOR_MULTIPLIER for elem in self.relevant]

		else:
			features = [0 for elem in self.relevant]

		return features

