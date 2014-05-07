from corpora import CorporaCreator
from helpers.classification import Classification
from helpers import Configuration
from helpers.reader import TruthParser

import tempfile, subprocess, sys

class BasicClassifier:

	def __init__(self, library, corpus_symbols = None):
		self.library = library
		self.corpora_creator = CorporaCreator(corpus_symbols)
		self.corpora = None
	
	def __getstate__(self):
		return self.corpora, self.library
	
	def __setstate__(self, state):
		self.corpora, self.library = state
	
	def create_corpora(self, data_reader):

		print 'Creating corpora...'
		for data, classification in data_reader:
			self.corpora_creator.feed_data(data, classification)
		
		self.corpora = self.corpora_creator.get_corpora()
		print '   DONE!'
		
	@staticmethod
	def get_model_file(file_name, file_name_suffix, file_ext):
		hyphen = ('-' if file_name_suffix else '')
		return Configuration.ModelDirectory + '/' + file_name + hyphen + file_name_suffix + '.' + file_ext

	def perform_training(self, data_reader, suffix, category_expander):

		print 'Creating train data file, suffix="' + suffix + '"...'
		train_data = open(self.get_model_file('train-data', suffix, 'dat'), 'w')
		
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
		scale_params_name = self.get_model_file('scale', suffix, 'params')
		input_name = train_data.name
		scaled_name = self.get_model_file('train-data-scaled', suffix, 'dat')
		self.library.scale(scale_params_name, input_name, scaled_name)
		print '   DONE!'
		
		print 'Training...'
		input_name = scaled_name
		results_name = self.get_model_file('train-results', suffix, 'dat')
		self.library.train(input_name, results_name)
		print '   DONE!'

	def train(self, data_reader):
		raise 'Not implemented'

	def strip_author_specs(self, data_reader):

		return [x[0] for x in data_reader]

	def perform_prediction(self, data_reader, suffix):

		print 'Creating prediction data file, suffix="' + suffix + '"...'
		classification_data = open(self.get_model_file('classification-data', suffix, 'dat'), 'w')
		
		j = 1
		for x in data_reader:

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
		scale_params_name = self.get_model_file('scale', suffix, 'params')
		input_name = classification_data.name
		scaled_name = self.get_model_file('classification-data-scaled', suffix, 'dat')		
		self.library.scale(scale_params_name, input_name, scaled_name)
		print '   DONE!'

		print 'Predicting...'
		input_name = scaled_name
		train_results_name = self.get_model_file('train-results', suffix, 'dat')
		results_name = self.get_model_file('result', suffix, 'dat')	
		self.library.predict(input_name, train_results_name, results_name)
		print '   DONE!'

		cls_numbers = map(int, open(results_name).readlines())
		return cls_numbers

	def compare_to_truth_if_present(self, cls_numbers, truth_file_name, author_specs):
		if truth_file_name:
			truth = TruthParser.parse(truth_file_name)
			total = len(truth)
			equal = 0
			for (author_spec, cls_number) in zip(author_specs, cls_numbers):
				author_id = author_spec[0]
				actual_cls_number = truth[author_id].to_int()
				if cls_number == actual_cls_number:
					equal += 1
			percent_equal = float(equal) / total * 100
			print 'Accuracy (checked at classify.py):', percent_equal, '% (', equal, '/', total, ')'

	def classify(self, data_reader, truth_file_name = None):
		raise 'Not implemented'


class JointClassifier(BasicClassifier):

	def __init__(self, library, corpus_symbols = None):
		BasicClassifier.__init__(self, library, corpus_symbols)

	def train(self, data_reader):

		self.create_corpora(data_reader)

		category_identity = lambda x: x
		self.perform_training(data_reader, suffix = '', category_expander = category_identity)

	def classify(self, data_reader, truth_file_name = None):

		author_specs = self.strip_author_specs(data_reader)

		cls_numbers = self.perform_prediction(data_reader, suffix = '')
		self.compare_to_truth_if_present(cls_numbers, truth_file_name, author_specs)

		clses = [Classification.from_int(cls_number) for cls_number in cls_numbers]

		return zip(author_specs, clses)


class DisjointClassifier(BasicClassifier):

	def __init__(self, library, corpus_symbols = None):
		BasicClassifier.__init__(self, library, corpus_symbols)

	def train(self, data_reader):

		self.create_corpora(data_reader)

		category_gender = Classification.unified_to_gender_int
		self.perform_training(data_reader, suffix = 'gender', category_expander = category_gender)

		category_age = Classification.unified_to_age_int
		self.perform_training(data_reader, suffix = 'age', category_expander = category_age)

	def classify(self, data_reader, truth_file_name = None):

		author_specs = self.strip_author_specs(data_reader)

		gender_cls_numbers = self.perform_prediction(data_reader, suffix = 'gender')
		age_cls_numbers = self.perform_prediction(data_reader, suffix = 'age')

		unify = Classification.gender_age_ints_to_unified
		unified_cls_numbers = [ unify(gender, age) for gender, age in zip(gender_cls_numbers, age_cls_numbers) ]

		self.compare_to_truth_if_present(unified_cls_numbers, truth_file_name, author_specs)
		clses = [Classification.from_int(cls_number) for cls_number in unified_cls_numbers]

		return zip(author_specs, clses)

