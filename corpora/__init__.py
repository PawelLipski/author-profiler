from helpers.interfaces import *
from corpora.trigrams import *


class CorporaCreator(CorpusCreator):
	def __init__(self):
		self.corpus_creators = [
			#FunctionWordsCorpusCreator(),
			#PartOfSpeechCorpusCreator(),
			HighestInfogainTrigramsCorpusCreator(),
			#HighestInfogainWordsCorpusCreator()
		]
	
	def feed_data(self, data, classification):
		for i in self.corpus_creators:
			i.feed_data(data, classification)
	
	def get_corpora(self):
		return Corpora([x.create_corpus() for x in self.corpus_creators])

class Corpora(Corpus):
	def __init__(self, corpora = []):
		self.corpora = corpora
	
	def __getstate__(self):
		return self.corpora
	
	def __setstate__(self, state):
		self.corpora = state
	
	def get_features_for_data(self, data):
		features_vector = []
		
		for corpus in self.corpora:
			features_vector += corpus.get_features_for_data(data)
		
		return features_vector

