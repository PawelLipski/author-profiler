from corpora import CorporaCreator
from helpers.classification import Classification

import tempfile, subprocess, sys

class Classifier:
	def __init__(self):
		self.corpora_creator = CorporaCreator()
		self.corpora = None
	
	def __getstate__(self):
		return self.corpora
	
	def __setstate__(self, state):
		self.corpora = state
	
	def train(self, data_reader):
		for data, classification in data_reader:
			self.corpora_creator.feed_data(data, classification)
		
		self.corpora = self.corpora_creator.get_corpora()
		train_data = open('train_data.dat', 'w') #tempfile.NamedTemporaryFile()
		
		for data, classification in data_reader:
			features = self.corpora.get_features_for_data(data)
			
			train_data.write(str(classification.to_int()))
			for i in range(len(features)):
				train_data.write(' '+str(i+1)+':'+str(features[i]))
			train_data.write("\n")
		
		train_data.flush()
		
		result = subprocess.check_call(['svm-train', train_data.name, 'train-results.dat'])
	
	def classify(self, data):
		classification_data = open('classification_data.dat', 'w') #tempfile.NamedTemporaryFile()
		
		features = self.corpora.get_features_for_data(data)
		classification_data.write('1')
		#sys.stdout.write('1')
		for i in range(len(features)):
			classification_data.write(' '+str(i+1)+':'+str(features[i]))
			#sys.stdout.write(' '+str(i+1)+':'+str(features[i]))
		classification_data.write("\n")
		#sys.stdout.write("\n")
		classification_data.flush()
		
		result = open('result.dat', 'w+') #tempfile.NamedTemporaryFile('r')
		
		subprocess.check_call(['svm-predict', classification_data.name, 'train-results.dat', result.name])
		
		return Classification.from_int(int(result.read(16)))
		