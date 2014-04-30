
class PredictionWriter:

	@staticmethod
	def output_prediction(outdir, authorid, cls):

		gender, age = str(cls).split(', ')
		tag = """
		<author id="%s"
			type="blog|twitter|socialmedia|reviews"
			lang="en|es"
			age_group="%s"
			gender="%s"
		/>""" % (authorid, age, gender)

		out = open(outdir + '/' + authorid + '.xml', 'w')
		out.write(tag)
		out.close()

