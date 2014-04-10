from helpers.reader import DataReader 
from helpers.classifier import Classifier

import pickle
import sys

if len(sys.argv) < 2:
	print 'Usage: %s xml_dir' % sys.argv[0]
	sys.exit(1)

classifier = Classifier()

reader = DataReader(sys.argv[1] + '*.xml')
classifier.train(reader)

file = open('classifier.dat', 'w')
pickle.dump(classifier, file)
file.close()