
class PredictionWriter:

	@staticmethod
	def output_prediction(outdir, authorspec, cls):

		authorid, lang = authorspec
		gender, age = str(cls).split(', ')
		# TODO: hard-coded blog!
		tag = """<author id="%s"
		type="blog"
		lang="%s"
		age_group="%s"
		gender="%s"/>\n""" % (authorid, lang, age, gender)

		out = open(outdir + '/' + authorid + '.xml', 'w')
		out.write(tag)
		out.close()

