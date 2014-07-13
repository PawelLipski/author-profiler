import re
import nltk

from helpers.interfaces import *
from helpers.utils import AutoDict
from textprocess.splitters import *

VECTOR_MULTIPLIER = 1000

class ElementsFrequencyCorpus(Corpus):
	
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
			
			features = [float(given_frequency[elem])/len(given)*VECTOR_MULTIPLIER for elem in self.relevant]
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
		flattened = [freqs[gram] for gram in most_common]
		gram_count = sum(flattened)
		scaled = [x / gram_count * VECTOR_MULTIPLIER for x in flattened]
		return scaled
	
	def get_features_for_data(self, data):
		words = WordSplitter.split(data)
		poses = nltk.pos_tag(words)
		
		prev_pos = None
		
		for cur_pos in poses:
			self.unigram_freqs[cur_pos] += 1
			if prev_pos != None:
				self.bigram_freqs[(prev_pos, cur_pos)] += 1
			prev_pos = cur_pos
		
		unigram_features = self.flatten_features(self.unigrams_most_common, self.unigram_freqs)
		bigram_features = self.flatten_features(self.bigrams_most_common, self.bigram_freqs)
		
		return unigram_features + bigram_features

class SentenceLengthCorpus(Corpus):
	def __init__(self):
		pass
	
	def __getstate__(self):
		pass
	
	def __setstate__(self, state):
		pass
	
	def get_features_for_data(self, data):
		sentences = [
			len(i.strip())
				for i in data.replace('!', '.').replace('?', '.').split('.')
					if len(i.strip()) > 0
		]
		if len(sentences) == 0:
			return [0]
		else:
			return [reduce(lambda x, y: x + y, sentences) / len(sentences)]

class SentenceWordsCorpus(Corpus):
	def __init__(self):
		pass
	
	def __getstate__(self):
		pass
	
	def __setstate__(self, state):
		pass
	
	def get_features_for_data(self, data):
		words = [
			len([1 for j in i.strip().split(' ') if len(j) > 0])
				for i in data.replace('!', '.').replace('?', '.').split('.')
					if len(i.strip()) > 0
		]
		if len(words) == 0:
			return [0]
		else:
			return [reduce(lambda x, y: x + y, words) / len(words)]
