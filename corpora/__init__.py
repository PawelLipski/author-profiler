
from helpers.interfaces import *
from creators import *


class CorporaCreator(CorpusCreator):
	CREATORS = {
		 'FW': FunctionWordsCorpusCreator,
		'POS': PartOfSpeechCorpusCreator,
		'CNG': HighestInfogainTrigramsCorpusCreator,
		 'CW': HighestInfogainWordsCorpusCreator,
		'LEN': SentenceLengthCorpusCreator,
		'WRD': SentenceWordsCorpusCreator,
	}
	
	def __init__(self, corpus_symbols = None):
		if corpus_symbols == None:
			corpus_symbols = self.CREATORS.keys()
		
		self.corpus_creators = [ 
			self.CREATORS[corpus_symbol]() for corpus_symbol in corpus_symbols
		]
	
	def feed_data(self, data, classification):
		for i in self.corpus_creators:
			i.feed_data(data, classification)
	
	def get_corpora(self):
		print '   Creating corpora...'
		corpora_data = []
		for x in self.corpus_creators:
			print '      running ' + x.__class__.__name__
			corpora_data.append(x.create_corpus())
		print '      DONE!'
		
		return Corpora(corpora_data)

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

