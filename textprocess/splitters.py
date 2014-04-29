
import re

from helpers.interfaces import TextSplitter

class TrigramSplitter(TextSplitter):
	expr = re.compile("[\W\d_]+", re.UNICODE)
	
	@staticmethod
	def split(data):
		def _split(data):
			data = TrigramSplitter.expr.sub('', data.lower())

			current_word = ''
			for character in data:
				current_word = (current_word + character)[-3:]

				if len(current_word) < 3:
					continue

				yield current_word

		return list(_split(data))


class WordSplitter(TextSplitter):
	expr = re.compile('[^\s\w]+', re.UNICODE)
	
	@staticmethod
	def split(data):
		data = WordSplitter.expr.sub('', data.lower())
		return data.split()
