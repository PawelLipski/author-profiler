
from cw import *

def compute_corpus_wide_stats(articles, corp_procs):

	for (article, classification) in articles:

		for corp_proc in corp_procs:
			corp_proc.switch_article(classification)

		for w in article.split(' '):
			for corp_proc in corp_procs:
				corp_proc.record_word(w)
			for c in w:
				for corp_proc in corp_procs:
					corp_proc.record_char(c)


def pass_stats_to_article_processors(procs):
	for (corp_proc, art_proc) in procs:
		stats = corp_proc.get_corpus_wide_stats()
		art_proc.set_corpus_wide_stats(stats)


def compute_feature_vectors_for_articles(articles, art_procs):
	for (article, _) in articles:

		for w in article.split(' '):
			for art_proc in art_procs:
				art_proc.record_word(w)
			for c in w:
				for art_proc in art_procs:
					art_proc.record_char(c)

		for art_proc in art_procs:
			v = art_proc.get_features()
			art_proc.clean_up()


def main():

	procs = [ (CWCorpusProcessor(), CWArticleProcessor()) ]
	articles = [ (open("lorem.txt").read(), 1) ]

	corp_procs = [corp_proc for (corp_proc, art_proc) in procs]
	compute_corpus_wide_stats(articles, corp_procs)

	pass_stats_to_article_processors(procs)

	art_procs = [art_proc for (corp_proc, art_proc) in procs]
	compute_feature_vectors_for_articles(articles, art_procs)

if __name__ == '__main__':
	main()
