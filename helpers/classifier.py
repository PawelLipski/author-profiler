from corpora import CorporaCreator
from helpers.classification import Classification

import tempfile, subprocess, sys

class Classifier:
	def __init__(self, corpus_symbols):
		self.corpora_creator = CorporaCreator(corpus_symbols)
		self.corpora = None
	
	def __getstate__(self):
		return self.corpora
	
	def __setstate__(self, state):
		self.corpora = state
	
	def train(self, data_reader):
		for data, classification in data_reader:
			self.corpora_creator.feed_data(data, classification)
		
		self.corpora = self.corpora_creator.get_corpora()
		train_data = open('train-data.dat', 'w') 
		#train_data = tempfile.NamedTemporaryFile()
		
		for data, classification in data_reader:
			features = self.corpora.get_features_for_data(data)
			
			train_data.write(str(classification.to_int()))
			for i in range(len(features)):
				train_data.write(' '+str(i+1)+':'+str(features[i]))
			train_data.write("\n")
		
		train_data.flush()
		
		result = subprocess.check_call(['svm-train', '-q', train_data.name, 'train-results.dat'])
	
	def classify(self, data_reader):

		classification_data = open('classification-data.dat', 'w')
		#classification_data = tempfile.NamedTemporaryFile()
		#classification_data.write(str(len(data_set)) + "\n")

		for data, classification in data_reader:
			features = self.corpora.get_features_for_data(data)
			classification_data.write(str(classification.to_int()) + ' ')
			for i in range(len(features)):
				value = str(i+1)+':'+str(features[i])+' '
				classification_data.write(value)
			classification_data.write("\n")
		classification_data.flush()		

		result_file = open('result.dat', 'w+') 
		#result = tempfile.NamedTemporaryFile('r')
		subprocess.check_call(['svm-predict', classification_data.name, 'train-results.dat', result_file.name])

		results = map(int, result_file.readlines())
		return [Classification.from_int(cls) for cls in results]
		
