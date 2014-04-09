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
		self.trigrams_clasification = AutoDict(AutoDict)
		self.articles_clasification = AutoDict()
	
	def feed_data(self, data, clasification):
		data = TextNormalizerProcessor.process(data)
		
		article_trigrams = dict()
		
		current_word = ''
		for character in data:
			current_word = (current_word + character)[-3:]
			
			if len(current_word) < 3:
				continue
			
			article_trigrams[current_word] = 1
			self.trigrams_frequency[current_word] += 1
		
		self.articles_clasification[clasification.to_int()] += 1
		for trigram in article_trigrams:
			self.trigrams_clasification[trigram][clasification.to_int()] += 1
	
	def create_corpus(self):
		trigrams_freq_sorted = sorted(self.trigrams_frequency.iteritems(), key=operator.itemgetter(1))
		trigrams_infogain = [
			(x[0], InformationGainMetric.get_infogain(self.articles_clasification, self.trigrams_clasification[x[0]]))
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
