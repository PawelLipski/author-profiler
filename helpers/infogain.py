
from math import log

class InformationGainMetric:

	@staticmethod
	def get_infogain(elements_per_category, featured_per_category):
		log2_or_zero = lambda x: log(x, 2) if x else 0.0
		div_or_zero = lambda m, n: (float(m) / n) if n else 0.0
		
		total = sum(elements_per_category.values())
		total_containing_the_word = sum(featured_per_category.values()) # sum over categories
		total_not_containing_the_word = total - total_containing_the_word
		#print total, total_containing_the_word, total_not_containing_the_word 
		
		entropy_in_arts_containing_the_word = 0.0
		for category in featured_per_category.keys():
			in_category_containing = featured_per_category[category]
			prop_containing_is_in_category = div_or_zero(in_category_containing, total_containing_the_word)
			entropy_in_arts_containing_the_word += (((-1))) * prop_containing_is_in_category \
							* log2_or_zero(prop_containing_is_in_category)
		
		prop_art_contains_the_word = div_or_zero(total_containing_the_word, total)
		
		
		entropy_in_arts_not_containing_the_word = 0.0
		for category in featured_per_category.keys():
			in_category_not_containing = elements_per_category[category] - featured_per_category[category]
			prop_not_containing_is_in_category = div_or_zero(in_category_not_containing, total_not_containing_the_word)
			entropy_in_arts_not_containing_the_word += (((-1))) * prop_not_containing_is_in_category \
							* log2_or_zero(prop_not_containing_is_in_category)
		
		prop_art_doesnt_contain_the_word = div_or_zero(total_not_containing_the_word, total)
		
		#print featured_per_category
		#print prop_art_contains_the_word, entropy_in_arts_containing_the_word, \
		#	 prop_art_doesnt_contain_the_word, entropy_in_arts_not_containing_the_word
		
		ig = - prop_art_contains_the_word * entropy_in_arts_containing_the_word \
			 - prop_art_doesnt_contain_the_word * entropy_in_arts_not_containing_the_word
		return ig

