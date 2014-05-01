from corpora import CorporaCreator
from helpers.classification import Classification
from helpers import Configuration

import tempfile, subprocess, sys

class Classifier:
	def __init__(self, corpus_symbols = None):
		self.corpora_creator = CorporaCreator(corpus_symbols)
		self.corpora = None
	
	def __getstate__(self):
		return self.corpora
	
	def __setstate__(self, state):
		self.corpora = state
	
	def create_corpora(self, data_reader):

		print 'Creating corpora...'
		for data, classification in data_reader:
			self.corpora_creator.feed_data(data, classification)
		
		self.corpora = self.corpora_creator.get_corpora()
		print '   DONE!'
		
	def perform_training(self, data_reader, file_name_suffix, category_expander):

		def get_model_file(file_name, file_ext):
			hyphen = ('-' if file_name_suffix else '')
			return Configuration.ModelDirectory + '/' + file_name + hyphen + file_name_suffix + '.' + file_ext

		print 'Creating train data file...'
		train_data = open(get_model_file('train-data', 'dat'), 'w')
		
		for data, classification in data_reader:
			features = self.corpora.get_features_for_data(data)
			
			expanded_category = category_expander(classification.to_int())
			train_data.write(str(expanded_category))
			for i in range(len(features)):
				if features[i] != 0:
					train_data.write(' '+str(i+1)+':'+str(features[i]))
			train_data.write("\n")
		
		train_data.flush()
		train_data.close()
		print '   DONE!'
		
		print 'Scaling values...'
		scaled_data = open('train-data-scaled.dat', 'w')
		subprocess.check_call(['svm-scale', '-l', '0', '-s', get_model_file('scale', 'params'), train_data.name],
			stdout=scaled_data)
		scaled_data.flush()
		print '   DONE!'
		
		print 'Training...'
		result = subprocess.check_call(['svm-train', scaled_data.name, get_model_file('train-results', 'dat')])
		print '   DONE!'

	def train(self, data_reader):

		self.create_corpora(data_reader)

		category_identity = lambda x: x
		self.perform_training(data_reader, file_name_suffix = '', category_expander = category_identity)
		
	
	def classify(self, data_reader):
		print 'Creating prediction data file...'
		classification_data = open('classification-data.dat', 'w')
		#classification_data = tempfile.NamedTemporaryFile()
		#classification_data.write(str(len(data_set)) + "\n")
		
		j = 1
		authorspecs = []
		for x in data_reader:

			authorspec = x[0]
			authorspecs += [authorspec]
			data = x[1]
			
			features = self.corpora.get_features_for_data(data)
			classification_data.write(str(j) + ' ')
			for i in range(len(features)):
				if features[i] != 0:
					value = str(i+1)+':'+str(features[i])+' '
					classification_data.write(value)
			classification_data.write("\n")
			j += 1
		
		classification_data.flush()
		classification_data.close()
		print '   DONE!'

		print 'Scaling values...'
		scaled_data = open('classification-data-scaled.dat', 'w')
		subprocess.check_call(['svm-scale', '-l', '0', '-r', Configuration.ModelDirectory+'/scale.params', classification_data.name],
			stdout=scaled_data)
		scaled_data.flush()
		print '   DONE!'

		print 'Predicting...'
		result_file = open('result.dat', 'w+')
		subprocess.check_call(['svm-predict', scaled_data.name, Configuration.ModelDirectory+'/train-results.dat', result_file.name])
		print '   DONE!'

		results = map(int, result_file.readlines())
		clses = [Classification.from_int(cls) for cls in results]

		return zip(authorspecs, clses)
		
