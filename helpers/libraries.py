
import subprocess

class LibraryWrapper:

	def scale(self, scale_params_name, input_name, scaled_name):
		raise 'Not implemented'

	def train(self, input_name, results_name):
		raise 'Not implemented'

	def predict(self, input_name, train_results_name, results_name):
		raise 'Not implemented'


class LibsvmWrapper(LibraryWrapper):
	
	def scale(self, scale_params_name, input_name, scaled_name):

		scaled = open(scaled_name, 'w')
		subprocess.check_call(['svm-scale', '-l', '0', '-s', scale_params_name, input_name], stdout=scaled)
		scaled.close()

	def train(self, input_name, results_name):
		subprocess.check_call(['svm-train', input_name, results_name])

	def predict(self, input_name, train_results_name, results_name):
		subprocess.check_call(['svm-predict', input_name, train_results_name, results_name])

class LiblinearWrapper(LibraryWrapper):
	
	def scale(self, scale_params_name, input_name, scaled_name):
		subprocess.check_call(['cp', input_name, scaled_name])

	def train(self, input_name, results_name):
		subprocess.check_call(['linear-train', input_name, results_name])

	def predict(self, input_name, train_results_name, results_name):
		subprocess.check_call(['linear-predict', input_name, train_results_name, results_name])

