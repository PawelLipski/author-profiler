#!/usr/bin/env python

import argparse
parser = argparse.ArgumentParser(description='Creates model for author profiling using given corpus.')
parser.add_argument('-i', metavar='corpus_dir', required=True, help='path to dir containing *.xml files')
parser.add_argument('-o', metavar='model_dir', required=True, help='path to empty dir where model will be saved')
parser.add_argument('--disjoint', action='store_true', help='if present, forces use of disjoint (gender/age) classifier;' +\
	' otherwise, joint classifier is used')
parser.add_argument('--liblinear', action='store_true', help='if present, forces use of liblinear;' +\
	' otherwise, libsvm is used')
args = parser.parse_args()

from helpers import Configuration
Configuration.CorpusDirectory = args.i
Configuration.ModelDirectory = args.o

from helpers.reader import TrainDataReader
from helpers.classifier import *
from helpers.libraries import *

import pickle
import sys
import os.path

library = LiblinearWrapper() if args.liblinear else LibsvmWrapper()
classifier = DisjointClassifier(library) if args.disjoint else JointClassifier(library)

if os.path.isfile(Configuration.CorpusDirectory + '/truth.txt'):
	reader = TrainDataReader(Configuration.CorpusDirectory + '/*.xml', Configuration.CorpusDirectory + '/truth.txt')
else:
	reader = TrainDataReader(Configuration.CorpusDirectory + '/*.xml')

classifier.train(reader)

file = open(Configuration.ModelDirectory + '/classifier.dat', 'w')
pickle.dump(classifier, file)
file.close()

