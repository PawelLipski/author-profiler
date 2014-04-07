from helpers.interfaces import TextProcessor
import re

class TagsStripperProcessor(TextProcessor):
	@staticmethod
	def process(text):
		return re.sub(r'<[^>]*?>', '', text)
