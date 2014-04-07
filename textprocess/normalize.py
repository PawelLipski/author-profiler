# -*- encoding: utf-8 -*-

from helpers.interfaces import TextProcessor
import re

class TextNormalizerProcessor(TextProcessor):
	@staticmethod
	def process(text):
		return re.sub('[.,;?!-_\r\n\t \'\"\\/\[\]*]', '', text.lower())
