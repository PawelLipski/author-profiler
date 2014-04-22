from helpers.reader import DataReader

import pickle
import sys

if len(sys.argv) < 2:
	print 'Usage: %s xml_file' % sys.argv[0]
	sys.exit(1)

file = open('classifier.dat', 'r')
classifier = pickle.load(file)
file.close()

reader = MixedDataReader(sys.argv[1] + '*.xml')
authorids, data_set, expected = zip(*reader)
predicted = classifier.classify(reader)

for i in xrange(0, len(predicted)):
	print 'Author:', authorids[i], 'is', expected[i], 'predicted', predicted[i]
 
