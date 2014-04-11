from helpers.reader import DataReader

import pickle
import sys

if len(sys.argv) < 2:
	print 'Usage: %s xml_file' % sys.argv[0]
	sys.exit(1)

file = open('classifier.dat', 'r')
classifier = pickle.load(file)
file.close()

reader = DataReader(sys.argv[1])
data, expected = reader.__iter__().next()

print 'Expected: ' + str(expected)
predicted = classifier.classify(data)
print 'Predicted: ' + str(predicted)
print 'SAME' if expected.to_int() == predicted.to_int() else 'DIFFERENT'

