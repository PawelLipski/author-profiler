#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description='Creates model for author profiling using given corpus.')
parser.add_argument('-i', metavar='corpus_dir', required=True, help='path to dir containing *.xml files')
parser.add_argument('-m', metavar='model_dir', required=True, help='path to dir containg model files')
parser.add_argument('-o', metavar='output_dir', required=True, help='path to dir where results will be saved')
args = parser.parse_args()

from helpers import Configuration
Configuration.CorpusDirectory = args.i
Configuration.ModelDirectory = args.m
Configuration.OutputDirectory = args.o

from helpers.reader import DataReader

import pickle
import sys

if len(sys.argv) < 2:
	print 'Usage: %s xml_file' % sys.argv[0]
	sys.exit(1)

file = open(Configuration.ModelDirectory + '/classifier.dat', 'r')
classifier = pickle.load(file)
file.close()

reader = ClassifyDataReader(sys.argv[1] + '*.xml')
authorids, data_set = zip(*reader)
predicted = classifier.classify(reader)

for i in xrange(0, len(predicted)):
	# TODO: save results
	pass

