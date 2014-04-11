from helpers.reader import DataReader

import pickle
import sys

if len(sys.argv) < 2:
	print 'Usage: %s xml_file' % sys.argv[0]
	sys.exit(1)

file = open('classifier.dat', 'r')
classifier = pickle.load(file)
file.close()

reader = DataReader(sys.argv[1] + '*.xml')
#data_set, expected = zip(*reader)

#print 'Expected: ' + str([c.to_int() for c in expected])
predicted = classifier.classify(reader)
#print 'Predicted: ' + str([c.to_int() for c in predicted])
#print 'SAME' if expected.to_int() == predicted.to_int() else 'DIFFERENT'

