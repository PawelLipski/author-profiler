import glob
import xml.dom.minidom as dom
from textprocess.tags import TagsStripperProcessor
from helpers.classification import Classification

class DataReader:
	def __init__(self, directory):
		self.path = directory
	
	def __iter__(self):
		def iterator():
			for file in glob.iglob(self.path):
				domo = dom.parse(file)
				
				gender = domo.documentElement.getAttribute('gender')
				age = domo.documentElement.getAttribute('age_group')
				classification = Classification(gender, age)
				
				conversations = domo.getElementsByTagName('conversation')
				for conversation in conversations:
					text = conversation.firstChild.nodeValue
					text = TagsStripperProcessor.process(text)
					yield text, classification
		
		return iterator()
