from utils import *
from perceptron import *

path = '/Users/happyhour/Documents/Perceptron/data'

features_test_no = readData(path,'test','no')
features_test_yes = readData(path,'test','yes')


features_train_no = readData(path,'train','no')
for f in features_train_no:
	f.append(-1.0)

features_train_yes = readData(path,'train','yes')
for f in features_train_yes:
	f.append(1.0)




data = features_train_no[:]
data.extend(features_train_yes)
test = features_test_no[:]
test.extend(features_test_yes)

for d in data:
	print d
print len(data)
for t in test:
	print t
p = Perceptron(data)
p.train(30)

for t in test:
	print p.predict(t)