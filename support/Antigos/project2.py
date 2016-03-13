#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn import svm
from sklearn import metrics
import nltk
import os
import sys
import time
import math


############################# TODO #############################
#
#     
#    
#
#------------------------------SVM------------------------------
#       
#     new words in test, how to handle that?
#
################################################################


class Discourse:

	def __init__(self,path,file_name,threshold=0,bigram=False):
		self.file_name = file_name
		self.path = path
		self.unigrams = self.tokenize(path+file_name) 
		self.bigrams = self.tokenize(path+file_name,bigram)
		self.score = -1
		self.threshold = threshold
		self.features = self.extractFeatures(True)



	def tokenize(self,path,bigram=False):
		file_data = open(path).read().decode('utf-8')
		tokens = nltk.word_tokenize(file_data)
		if bigram:
			return nltk.bigrams(tokens)

		return tokens

	def getScore(self):
		return self.score

	def setScore(self,score):
		self.score = score

	def getCategoricalScore(self):
		#best result G>=7, A>=4.5
		if self.score >= 7.0:
			return 'good'

		elif self.score >= 4.5:
			return 'average'
		else:
			return 'bad'

	def getDiscreteClass(self):
		clas = {"good":2,"average":1,"bad":0}

		return clas[self.getCategoricalScore()]

	def getTokens(self):
		return self.tokens

	def getFileName(self):
		return self.file_name.split('.')[0]

	def getVocabulary(self):
		return set(self.features.keys())

	def getVocabularySize(self):
		return len(self.getVocabulary())

	def getFeatures(self):
		return self.features

	def extractFeatures(self,bigram=False):
		
		unigramFeatures = {}
		bigramsFeatures = {}

		freq = dict(nltk.FreqDist(self.unigrams))

		for token,f in freq.iteritems():
			if f > self.threshold:
				unigramFeatures[token] = f
		
		if bigram:
			freq = dict(nltk.FreqDist(self.bigrams))

			for token,f in freq.iteritems():
				a,b = token
				#print a,b
				if b in unigramFeatures:
					bigramsFeatures[token] = f
					

			return bigramsFeatures

		else:
			return unigramFeatures
			



		# if len(relevantFeatures) == 0:
		# 	print freq
		# 	raise Exception("No one feature was extracted. Cut of %d is very high" % self.relevant_frequency)
		# else:
		# 	print "%d features were extracted" % len(relevantFeatures)
		
		

	def __str__(self):
		return "---%s---\nSize = %d Score = %1.2f\n %s " % (self.getFileName(), 
			self.getVocabularySize(),self.getScore(), self.getTokens())

class Classifier(object):

	def __init__(self,train_discourse,test_discourse,categorical=True):
		
		#-------------TRAIN------------
		self.train_data = train_discourse
		self.targetTrain = None
		self.targetTrain_mapped_score = None #{doc_name:score}

		#-------------TEST------------
		self.test_data = test_discourse
		self.targetTest = None
		self.targetTest_mapped_score = None #{doc_name:score}


		self.vocabulary_train = self.join_vocabulary(self.train_data)
		self.isCategorical = categorical
		self.features_mapped_row = self.mapping_features_row(self.vocabulary_train)#{word:row_index}
		
		self.classes = None
		self.startConfig()

	def startConfig(self):
	 	#{doc_name:score}

	 	if self.isCategorical:
	 		self.targetTrain_mapped_score = dict([(d.getFileName(),d.getCategoricalScore()) for d in self.train_data])
	 		self.targetTest_mapped_score = dict([(d.getFileName(),d.getCategoricalScore()) for d in self.test_data])
	 	else:
	 		self.targetTrain_mapped_score = dict([(d.getFileName(),d.getScore()) for d in self.train_data])
	 		self.targetTest_mapped_score = dict([(d.getFileName(),d.getScore()) for d in self.test_data])

	 	self.classes = list(set(self.targetTrain_mapped_score.values()))
	 	self.targetTest = self.gettarget(self.test_data)
		self.targetTrain = self.gettarget(self.train_data)




	def setCategoricalData(self,categorical=True):
		self.isCategorical = categorical
		self.startConfig()

	def getVocabularySize(self):
		return len(self.vocabulary_train)

	def mapping_features_row(self,vocabulary):
		features = list(vocabulary)
		features.sort()

		return dict([ (features[index],index)for index in xrange(len(features))])

	def join_vocabulary(self,discourses):
		features_overall = set()

		for discourse in discourses:
			features_overall = features_overall.union(discourse.getVocabulary())

		features_overall = list(features_overall)
		features_overall.sort()

		return features_overall

	def createRowFeatures(self,discourse):
		features_discourse = discourse.getFeatures()
		row = [0 for i in xrange(len(self.features_mapped_row))]
		
		for feature,value in features_discourse.iteritems():
			if feature in self.features_mapped_row: #TODO 
				row[self.features_mapped_row[feature]] = value

		return row

	def createMatrix(self,data):
		matrix = []
		time_count = time.time()
		for discourse in data:
			matrix.append(self.createRowFeatures(discourse))

		#print 'time spent to create a matrix of features %1.4f seconds' % (time.time()-time_count)
		return matrix

	def gettarget(self,data):
		if self.isCategorical:
			return [discourse.getCategoricalScore() for discourse in data]

		return [discourse.getScore() for discourse in data]

	def analizePerformance(self, estimated, target):
		TP_overall = 0
		P = 0
		

		class_predictions_correct   = dict([(clas,0) for clas in self.classes])
		class_predictions_incorrect = dict([(clas,{}) for clas in self.classes])

		if len(estimated) != len(target):
			print "estimated and target do not have the same size",len(estimated),len(target)
			return -1

		for index in xrange(len(estimated)):
			y = estimated[index]
			t = target[index]


			if y == t:
				class_predictions_correct[t] += 1
			else:
				if y not in class_predictions_incorrect[t]:
					class_predictions_incorrect[t][y] = []

				class_predictions_incorrect[t][y].append(index)

		
		for clas in self.classes:
			TP = class_predictions_correct[clas]
			FN = []

			for v in class_predictions_incorrect[clas].values():
				FN.extend(v)
			FP = 0
			TN = 0

			
			for key_, value_ in class_predictions_incorrect.iteritems():
				if key_ != clas:
					if clas in value_:
						FP += len(value_[clas])

				for c, v in value_.iteritems():
					if c != clas:
						TN += len(v)

			accuracy = (TP + TN)/float((TP+TN+FP+len(FN)))
			precision = (TP+0.0001)/(float(TP+FP)+0.0001)
			recall =  TP/float(TP + len(FN))


			# print '-------------%s-------------\nAC %1.3f |P %1.3f |R %1.3f |F1 %1.3f' % \
			# 							(clas, accuracy,precision,recall,
			# 								(2*(precision*recall)/(precision + recall)))

			#print '%s\nTP=[%d]\nFN=[%d]\nFP=[%d]\nTN=[%d]\n' % ('-'*20,TP, len(FN), FP, TN)

			P += precision*((TP+len(FN))/float(len(estimated)))
			TP_overall += TP

		accuracy = TP_overall/float(len(estimated))
		recall = metrics.recall_score(target,estimated)
		precision = metrics.recall_score(target,estimated)
		F1 = 2*(P*recall/(P + recall))

		
		print 'Accuracy  = %1.4f' % accuracy
		print 'Precision = %1.4f' % P
		print 'Recall    = %1.4f' % recall
		print 'F1        = %1.4f' % F1

		print precision,P
		return {"Accuracy":accuracy,"Precision":P,"Recall":recall,"F1":F1}
		
	def train(self):
		pass

	def test(self,discourse):
		pass

class NaiveBayes(Classifier):

	
	def __init__(self,train_discourse,test_discourse):
		super(NaiveBayes, self).__init__(train_discourse,test_discourse)
		self.map_class_tokens, self.prior = self.getMapClassTokens()
		self.map_class_tokens_prob = None

	def train(self):
		self.map_class_tokens_prob = {}
		

		for clas, tokens in self.map_class_tokens.iteritems():

			if clas not in self.map_class_tokens_prob:
				self.map_class_tokens_prob[clas] = {}
			
			for token,freq in tokens.iteritems():

				if token not in self.map_class_tokens_prob[clas]:
					probability_t_c = self.probTokenGivenClassSmoothing(token,clas,self.getVocabularySize())
					self.map_class_tokens_prob[clas][token] = probability_t_c

		#print '---NaiveBayes trained---'
		
	def test_one(self,discourse):

		if self.map_class_tokens_prob == None:
			return 'No results. No train was made'

		discourse_features = discourse.getFeatures()
		results = []
		for clas in self.classes:
			result = self.prior[clas]

			for feature,count in discourse_features.iteritems():
				if feature in self.map_class_tokens_prob[clas]:
					result *= math.log(self.map_class_tokens_prob[clas][feature])**count
				else:	
					result *= math.log(self.probTokenGivenClassSmoothing(feature,
												clas,self.getVocabularySize()))
			results.append((result,clas))

		results.sort()

		return results[-1][1]

	def test(self):
		accuracy = 0
		predictions = []
		self.targetTest

		for discourse in self.test_data:
			predictions.append(self.test_one(discourse))

		print '-----------------Naive Bayes--------------------'
		return self.analizePerformance(predictions, self.targetTest)
		

	def getMapClassTokens(self):
		map_clas_tokens = {}
		clas_discourses = {}


		for discourse in self.train_data:
			discourse_features = discourse.getFeatures()
			#clas = self.targetTrain_mapped_score[discourse.getFileName()] #TODO - why not discourse.getClass()
			clas = discourse.getCategoricalScore()
			
			if clas not in clas_discourses:
				clas_discourses[clas] = 0
			clas_discourses[clas] += 1


			for token,freq in discourse_features.iteritems():

				if clas not in map_clas_tokens:
					map_clas_tokens[clas] = {}

				if token not in map_clas_tokens[clas]:
					map_clas_tokens[clas][token] = 0


				map_clas_tokens[clas][token] += freq

		for clas, count in clas_discourses.iteritems():

			clas_discourses[clas] = float(count)/len(self.train_data)
			#print map_clas_tokens.keys()
			map_clas_tokens[clas]['___OVERALL___'] = sum(map_clas_tokens[clas].values())

		return map_clas_tokens,clas_discourses

	def countTokenGivenClass(self,token,clas):

		if token not in self.map_class_tokens[clas]:
			return 0

		return self.map_class_tokens[clas][token]

	def countTokenOverall(self,clas):
		return self.map_class_tokens[clas]['___OVERALL___']

	def probTokenGivenClass(self,token,clas):
		return self.countTokenGivenClass(token,clas)/float(self.countTokenGivenClass(token))

	def probTokenGivenClassSmoothing(self,token,clas,vocabularySize):

		A = self.countTokenGivenClass(token,clas) + 1
		B = self.countTokenOverall(clas) + vocabularySize

		return A/float(B)

	def __str__(self):
		return 'Vocabulary size = %d\nNumber of classes = %d\n' % (self.getVocabularySize(),len(self.prior))

class SVM(Classifier):


	def __init__(self,train_discourse,test_discourse):
		super(SVM, self).__init__(train_discourse,test_discourse)
		
		self.matrix_features_train = self.createMatrix(self.train_data)
		self.matrix_features_test = self.createMatrix(self.test_data)

		self.svm_classifier = svm.SVC() #svm.LinearSVC()
		self.clas_coded = dict([(self.classes[index],index) for index in xrange(len(self.classes))])
		self.target_train_coded = [ self.clas_coded[label] for label in self.targetTrain]
		self.target_test_coded = [ self.clas_coded[label] for label in self.targetTest]
		print len(self.vocabulary_train)

	def train(self):
		self.svm_classifier.fit(self.matrix_features_train,self.target_train_coded)

	def test(self):
		predicted = self.svm_classifier.predict(self.matrix_features_test)
		estimated = []

		for p in predicted:
			estimated.append(self.classes[p])

		print '--------------------SVM--------------------'
		return self.analizePerformance(estimated, self.targetTest)

class Project:

	def __init__(self,threshold,bigram=False):
		self.PATH = os.getcwd()+'/talks/'
		self.PATH_TRAIN = self.PATH + 'train/'
		self.PATH_TEST = self.PATH + 'test/'
		self.threshold = threshold
		self.discourses_train = self.extract_data(self.PATH_TRAIN,threshold,bigram)
		self.discourses_test  = self.extract_data(self.PATH_TEST,0,bigram)
		self.statistics()


	def statistics(self):
		classes_train = {}
		classes_test = {}

		for index in xrange(len(self.discourses_train)):
			score = self.discourses_train[index].getCategoricalScore()

			if score not in classes_train:
				classes_train[score] = 0

			classes_train[score] += 1

		for index in xrange(len(self.discourses_test)):
			score = self.discourses_test[index].getCategoricalScore()

			if score not in classes_test:
				classes_test[score] = 0

			classes_test[score] += 1

		# print 'Train:'
		# for clas, count in classes_train.iteritems():
		# 	print '----%s(%d|%1.2f%%)' % (clas,count,100*(count/float(sum(classes_train.values()))))

		# print 'Test:'
		# for clas, count in classes_test.iteritems():
		# 	print '----%s(%d|%1.2f%%)' % (clas,count,100*(count/float(sum(classes_test.values()))))

	def getTxtFiles(self,list_files):
		txt_files = []

		for file_name in list_files:
			if '.txt' in file_name:
				txt_files.append(file_name)

		return txt_files

	def extract_data(self,path,relevant_frequency=0,bigram=False):
		
		list_files = self.getTxtFiles(os.listdir(path))
		discourses = [ Discourse(path,file_name,threshold,bigram) for file_name in list_files]
		return self.ratingDiscourses_ratings(discourses)

	def ratingDiscourses_ratings(self,discourses):

		file_ratings = open(self.PATH+'ratings.txt').readlines()
		rating =  dict([(line.split()[0],float(line.split()[1])) for line in file_ratings ])

		for discourse in discourses:
			discourse.setScore(rating[discourse.getFileName()])

		return discourses

	def run_naiveBayes(self):
		naive = NaiveBayes(self.discourses_train,self.discourses_test)
		time_count = time.time()
		naive.train()
		return naive.test()
		#print 'Time spent to Train and Test the Naive Bayes Classifier = %1.2f seconds' % (time.time()-time_count)

	def runSVM(self):
		svm_classifier = SVM(self.discourses_train,self.discourses_test)
		time_count = time.time()
		svm_classifier.train()
		return svm_classifier.test()
		#print 'Time spent to Train and Test the SVM Classifier = %1.2f seconds' % (time.time()-time_count)



if "__main__":
	
	file_data = open('statistics.txt','w')

	file_data.write('time_NV;accuracy;precision;recall;F1;time_SVM;accuracy;precision;recall;F1\n')
	threshold = 7
	p = Project(threshold,True)
	file_data.write('%d;' % threshold)
	time_count = time.time()
	result_Bayes = [float(v) for v in p.run_naiveBayes().values()]
	time_total = time.time()-time_count
	file_data.write("%1.5f;%1.2f;%1.2f;%1.2f;%1.2f" % \
			(time_total,result_Bayes[0],result_Bayes[1],result_Bayes[2],result_Bayes[3]))
	#print 'Naive Bayes RUNTIME %1.2fs ' % (time.time()-time_count) 

	time_count = time.time()
	result_SVM = [float(v) for v in p.runSVM().values()]
	time_total = time.time()-time_count
	file_data.write(";%1.5f;%1.2f;%1.2f;%1.2f;%1.2f\n" % \
		(time_total,result_SVM[0],result_SVM[1],result_SVM[2],result_SVM[3]))
	#print 'SVM RUNTIME %1.2fs' % (time.time()-time_count) 


			
	#print len(clas.map_class_tokens_prob['average'])


	
	