import sys
import glob
import xml.dom.minidom as dom
from textprocess.tags import TagsStripperProcessor
from helpers.classification import Classification

class DataReader:
	def __init__(self, directory):
		self.path = directory
	
	def __iter__(self):
		def iterator():
			for no, file in enumerate(glob.iglob(self.path)):
				print no,
				sys.stdout.flush()
				domo = dom.parse(file)
				
				gender = domo.documentElement.getAttribute('gender')
				age = domo.documentElement.getAttribute('age_group')
				classification = Classification(gender, age)
				
				conversations = domo.getElementsByTagName('conversation')
				for conversation in conversations:
					child = conversation.firstChild
					if not (child is None):
						text = child.nodeValue
						text = TagsStripperProcessor.process(text)
						yield text, classification
			print 
		
		return iterator()
