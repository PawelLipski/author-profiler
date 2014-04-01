
class Classification:

	def __init__(self, gender, age):
		self.gender = gender
		self.age = age

	NUMBER_OF_CATEGORIES = 8

	CATEGORY_FOR_GENDER = { 'F': 0, 'M': 4 }
	CATEGORY_FOR_AGE = { 18: 0, 25: 1, 35: 2, 50: 3 }

	def get_category_number(self):
		return self.CATEGORY_FOR_GENDER[self.gender] + self.CATEGORY_FOR_AGE[self.age]
