#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description='Classifies given texts and prints out information.')
parser.add_argument('-i', metavar='corpus_dir', required=True, help='path to dir containing *.xml files')
parser.add_argument('-m', metavar='model_dir', required=True, help='path to dir containg model files')
args = parser.parse_args()

from helpers import Configuration
Configuration.CorpusDirectory = args.i
Configuration.ModelDirectory = args.m

from helpers.reader import MixedDataReader

import pickle
import sys
import os.path

file = open(Configuration.ModelDirectory + '/classifier.dat', 'r')
classifier = pickle.load(file)
file.close()

if os.path.isfile(Configuration.CorpusDirectory + '/truth.txt'):
	reader = MixedDataReader(Configuration.CorpusDirectory + '/*.xml', Configuration.CorpusDirectory + '/truth.txt')
else:
	reader = MixedDataReader(Configuration.CorpusDirectory + '/*.xml')

authorids, data_set, expected = zip(*reader)
predicted = classifier.classify(reader)

for i in xrange(0, len(predicted)):
	print 'Author:', authorids[i], 'is', expected[i], 'predicted', predicted[i]
 
