
import re
from helpers.interfaces import TextSplitter

PATTERN = re.compile('[.,;?!-_\r\n\t \'\"\\/\[\]*]')

class TrigramSplitter(TextSplitter):

	@staticmethod
	def split(data):

		data = PATTERN.sub('', data.lower())

		current_word = ''
		for character in data:
			current_word = (current_word + character)[-3:]

			if len(current_word) < 3:
				continue

			yield current_word

class WordSplitter(TextSplitter):

	@staticmethod
	def split(data):

		data = PATTERN.split(data.lower())
		data = filter(None, data)
		return data

