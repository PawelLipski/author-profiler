import sys
import glob
import os.path
import xml.dom.minidom as dom

from textprocess.tags import TagsStripperProcessor
from helpers.classification import Classification

class TrainDataReader:
	def __init__(self, directory, truth = None):
		self.path = directory
		self.truth = truth
	
	def __iter__(self):
		truthdata = dict()
		
		# Read "truth.txt" and get data
		if self.truth:
			with open(self.truth) as truthfile:
				for line in truthfile:
					line = line.strip().split(':::')
					if len(line) < 3:
						raise Exception('Invalid line in truth file: ' + (':::'.join(line)))
					truthdata[line[0]] = Classification(line[1], line[2])
		
		def iterator():
			files_num = len(glob.glob(self.path))
			i = 1
			for file in glob.iglob(self.path):
				print '   file ' + str(i) + ' out of '+ str(files_num)
				authorid = os.path.basename(file)
				if authorid.find('_') != -1:
					authorid = authorid.split('_', 2)[0]
				elif authorid.find('.') != -1:
					authorid = authorid.split('.', 2)[0]
				else:
					raise Exception('Invalid XML filename (cannot find author-id): ' + authorid)
				
				domo = dom.parse(file)
				
				if self.truth:
					classification = truthdata[authorid]
				else:
					gender = domo.documentElement.getAttribute('gender')
					age = domo.documentElement.getAttribute('age_group')
					classification = Classification(gender, age)
				
				documents = domo.getElementsByTagName('document')
				text = ''
				
				for document in documents:
					child = document.firstChild
					text += ' '+TagsStripperProcessor.process(child.nodeValue)
				
				yield text, classification
				i += 1
		
		return iterator()

class ClassifyDataReader:
	def __init__(self, directory):
		self.path = directory
	
	def __iter__(self):
		def iterator():
			files_num = len(glob.glob(self.path))
			i = 1
			for file in glob.iglob(self.path):
				print '   file ' + str(i) + ' out of '+ str(files_num)
				authorid = os.path.basename(file)
				lang = ''
				if authorid.find('_') != -1:
					authorid, lang = authorid.split('_', 2)[:2]
				elif authorid.find('.') != -1:
					authorid, lang = authorid.split('.', 2)[:2]
				else:
					raise Exception('Invalid XML filename (cannot find author-id): ' + authorid)
				
				domo = dom.parse(file)
				documents = domo.getElementsByTagName('document')
				text = ''
				
				for document in documents:
					child = document.firstChild
					text += ' '+TagsStripperProcessor.process(child.nodeValue)
				
				yield (authorid, lang), text
				i += 1
		
		return iterator()

class MixedDataReader:
	def __init__(self, directory, truth = None):
		self.path = directory
		self.truth = truth
	
	def __iter__(self):
		truthdata = dict()
		
		# Read "truth.txt" and get data
		if self.truth:
			with open(self.truth) as truthfile:
				for line in truthfile:
					line = line.strip().split(':::')
					if len(line) < 3:
						raise Exception('Invalid line in truth file: ' + (':::'.join(line)))
					truthdata[line[0]] = Classification(line[1], line[2])
		
		def iterator():
			files_num = len(glob.glob(self.path))
			i = 1
			for file in glob.iglob(self.path):
				print '   file ' + str(i) + ' out of '+ str(files_num)
				authorid = os.path.basename(file)
				if authorid.find('_') != -1:
					authorid = authorid.split('_', 2)[0]
				elif authorid.find('.') != -1:
					authorid = authorid.split('.', 2)[0]
				else:
					raise Exception('Invalid XML filename (cannot find author-id): ' + authorid)
				
				domo = dom.parse(file)
				
				if self.truth:
					classification = truthdata[authorid]
				else:
					gender = domo.documentElement.getAttribute('gender')
					age = domo.documentElement.getAttribute('age_group')
					classification = Classification(gender, age)
				
				documents = domo.getElementsByTagName('document')
				text = ''
				
				for document in documents:
					child = document.firstChild
					text += ' '+TagsStripperProcessor.process(child.nodeValue)
				
				yield authorid, text, classification
				i += 1
		
		return iterator()
