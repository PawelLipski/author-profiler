
class PredictionWriter:

	@staticmethod
	def output_prediction(outdir, authorspec, cls):

		authorid, lang = authorspec
		gender, age = str(cls).split(', ')
		tag = """<author id="%s"
		type="blog|twitter|socialmedia|reviews"
		lang="%s"
		age_group="%s"
		gender="%s"/>\n""" % (authorid, lang, age, gender)

		out = open(outdir + '/' + authorid + '.xml', 'w')
		out.write(tag)
		out.close()

