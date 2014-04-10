class Classification:
	NUMBER_OF_CATEGORIES = 6
	MODULO = 3
	
	GENDER_CATEGORIES = { 'male': 0, 'female': 1 }
	AGE_CATEGORIES = { '10s': 0, '20s': 1, '30s': 2 }
	
	GENDER_INVERSE = dict((v,k) for k, v in GENDER_CATEGORIES.items())
	AGE_INVERSE = dict((v,k) for k, v in AGE_CATEGORIES.items())
	
	def __init__(self, gender, age):
		self.classification = self.GENDER_CATEGORIES[gender]*self.MODULO + self.AGE_CATEGORIES[age]
	
	def to_int(self):
		return self.classification
	
	def __str__(self):
		age = self.classification % self.MODULO
		gender = self.classification / self.MODULO
		
		return self.GENDER_INVERSE[gender] + ', ' + self.AGE_INVERSE[age]
	
	@staticmethod
	def from_int(value):
		return Classification(Classification.GENDER_INVERSE[value / Classification.MODULO],
			Classification.AGE_INVERSE[value % Classification.MODULO])
