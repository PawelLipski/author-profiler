
import nltk
from textprocess.splitters import WordSplitter

class PartOfSpeechTagger:

	@staticmethod
	def pos_ngrams_for_chunk(chunk):

		words = WordSplitter.split(chunk)
		poses = nltk.pos_tag(words)
		pos_pairs = zip(poses[:-1], poses[1:])

		return poses, pos_pairs

