
from classification import *
from cwcng import *

def prepare_test_articles():
	contents = open("1984.txt").read()
	n = 50
	chunk_len = len(contents) / n
	arts = [0] * n
	for i in range(0,n-1):
		arts[i] = contents[chunk_len * i: chunk_len * (i+1)]
	arts[n-1] = contents[chunk_len * (n-1):]

	articles = []
	for i in range(0,n):
		articles.append((arts[i], Classification('M' if i <= n/2 else 'F', [18, 25, 35, 50][i % 4])))
	return articles

def record_article_into_all_processors(article, procs):

	for w in article.split(' '):
		for proc in procs:
			proc.record_word(w.lower())
		for c in w:
			for proc in procs:
				proc.record_char(c)

def get_class_short_name(obj):
	return str(obj.__class__).split('.')[-1]


def compute_corpus_wide_stats(articles, corp_procs):

	for (article, classification) in articles:

		for corp_proc in corp_procs:
			corp_proc.switch_article(classification)

		record_article_into_all_processors(article, corp_procs)


def pass_stats_to_article_processors(procs):

	for (corp_proc, art_proc) in procs:

		print get_class_short_name(corp_proc), '- corpus-wide stats:',
		stats = corp_proc.get_corpus_wide_stats()
		art_proc.set_corpus_wide_stats(stats)


def compute_feature_vectors_for_articles(articles, art_procs):

	for (article, clsfn) in articles:

		print 'Article:', clsfn.gender, clsfn.age
		record_article_into_all_processors(article, art_procs)

		for art_proc in art_procs:
			print get_class_short_name(art_proc), '- article-wide stats:', art_proc.get_features()
			art_proc.clean_up()

def main():

	procs = [
		(CWCorpusProcessor(), CWArticleProcessor()),
		(CNGCorpusProcessor(), CNGArticleProcessor())
	]
	articles = prepare_test_articles()

	corp_procs = [corp_proc for (corp_proc, art_proc) in procs]
	compute_corpus_wide_stats(articles, corp_procs)

	pass_stats_to_article_processors(procs)

	art_procs = [art_proc for (corp_proc, art_proc) in procs]
	compute_feature_vectors_for_articles(articles, art_procs)

if __name__ == '__main__':
	main()
