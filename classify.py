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
data, classification = reader.__iter__().next()

print 'Expected: ' + str(classification)
result = classifier.classify(data)
print 'Predicted: ' + str(result)