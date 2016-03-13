import os
import random
import nltk
import math
import time
from sklearn import metrics
from sequences import *
"""
	this class get a data processed in the following format
	({'the':230,'it':50....},label)
	
"""
class Classifier(object):

	
	def __init__(self,train_data,test_data,isCategorical=True):
		
		#-------------TRAIN------------
		self.train_data = train_data
		self.test_data = test_data
		
		self.isCategorical = isCategorical
		self.features = self.train_data.getVocabulary()
		self.features.sort()
		self.features_mapped_row = self.mapping_features_row()
		
		
		self.classes = self.train_data.getClasses()

	def getVocabularySize(self):
		return self.train_data.getVocabularySize()
		
	def mapping_features_row(self):

		return dict([ (self.features[index],index)for index in xrange(len(self.features))])

# 	def createRowFeatures(self,sample):
# 		features_sample = sample.getFeatures()
# 		row = [0 for i in xrange(len(self.features_mapped_row))]
# 		
# 		for feature,value in features_discourse.iteritems():
# 			if feature in self.features_mapped_row: #TODO 
# 				row[self.features_mapped_row[feature]] = value
# 
# 		return row

	def createMatrix(self,data):
		matrix = []
		time_count = time.time()
		for sample in data:
			matrix.append(self.createRowFeatures(sample))

		#print 'time spent to create a matrix of features %1.4f seconds' % (time.time()-time_count)
		return matrix

	def getLabels(self,data):
		return self.data.getTargetMapped().values()
	
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
			recall =  TP/float(TP + len(FN)+0.0001) #TODO possible division by zero?


			# print '-------------%s-------------\nAC %1.3f |P %1.3f |R %1.3f |F1 %1.3f' % \
			# 							(clas, accuracy,precision,recall,
			# 								(2*(precision*recall)/(precision + recall)))

			#print '%s\nTP=[%d]\nFN=[%d]\nFP=[%d]\nTN=[%d]\n' % ('-'*20,TP, len(FN), FP, TN)

			P += precision*((TP+len(FN))/float(len(estimated)))
			TP_overall += TP

		accuracy = TP_overall/float(len(estimated))
		# recall = metrics.recall_score(target,estimated)
# 		precision = metrics.recall_score(target,estimated)
		F1 = 2*(P*recall/(P + recall))

		
		print 'Accuracy  = %1.4f' % accuracy
		print 'Precision = %1.4f' % P
		print 'Recall    = %1.4f' % recall
		print 'F1        = %1.4f' % F1

		return {"Accuracy":accuracy,"Precision":P,"Recall":recall,"F1":F1}

class NaiveBayes(Classifier):

	
	def __init__(self,train_data,test_data,isCategorical=True):
		super(NaiveBayes, self).__init__(train_data,test_data,isCategorical)
		self.count_tk_in_c, self.prior = self.calculateProbabilities()
		self.p_tk_in_c = None
		self.quantity_samples = len(self.train_data.getSamples())


	def train(self):
		self.p_tk_in_c = {}
		

		for class_, tokenFreq in self.count_tk_in_c.iteritems():
			
			if class_ not in self.p_tk_in_c:
				self.p_tk_in_c[clas] = {}

			for token,freq in tokenFreq.iteritems():
				
				if token not in self.p_tk_in_c[class_]:
					self.p_tk_in_c[class_][token] = self.probTokenGivenClassSmoothing(token,class_)

		#print '---NaiveBayes trained---'
		
	def test_one(self,sample):

		if self.p_tk_in_c == None:
			return 'No results. No train was made'

		sample_freqTokens = sample.getFreqTokens()
		results = []
		for clas in self.classes:
			result = self.prior[clas]

			for token,freq in sample_freqTokens.iteritems():


 				if token in self.p_tk_in_c[clas]:
 				
 					#if the value is too short or too large the information is discarded
 					try:
 						product = math.log(self.p_tk_in_c[clas][token])**freq
 					except:
 						print self.p_tk_in_c[clas][token],math.log(self.p_tk_in_c[clas][token])
 					
 					
 					result += product
				#else:	
				#	result *= math.log(self.probTokenGivenClassSmoothing(feature,
				#								clas,self.getVocabularySize()))
			results.append((result,clas))

		results.sort()

		return results[-1]

	def test(self):
		accuracy = 0
		predictions = []

		for sample in self.test_data:
			predictions.append(self.test_one(sample))

		#print '-----------------Naive Bayes--------------------'
		
		# for index in range(len(self.test_data)):
# 			print self.test_data[index].getFileName(),self.test_data[index].getCategoricalScore(),predictions[index]
		
		return self.analizePerformance(predictions, self.targetTest)
		

	def calculateProbabilities(self):
		"""
			from http://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf
			P(c|d) <> P(c) Sum(P(tk|c))
			
			return P(tk|c) and P(c)

		"""
		#P(tk|c)
		count_tk_in_c = {} 
		#P(c)
		p_c = {} 

		for sample in self.train_data.getSamples():
			freq_tokens = sample.getFreqTokens()
			class_ = sample.getCategoricalScore()

			if class_ not in p_c:
				p_c[class_] = 0
			p_c[class_] += 1
	

			for token,freq in freq_tokens.iteritems():
				#print token
				if class_ not in count_tk_in_c:
					#print 'x'*30
					count_tk_in_c[class_] = {}
					#print map_class_tokens.keys()

				if token not in count_tk_in_c[class_]:
					count_tk_in_c[class_][token] = 0


				count_tk_in_c[class_][token] += freq
		#print map_class_tokens.keys()
		#compute P(c) and P(tk|c)
		for class_, count in p_c.iteritems():
			

			p_c[class_] = float(count)/len(self.train_data.getSamples())
			#print map_class_tokens.keys()
			count_tk_in_c[class_]['___ALLTOKENS___'] = sum(self.p_tk_in_c[class_].values())

		return count_tk_in_c,p_c

	def countTokenGivenClass(self,token,clas):

		if token not in self.count_tk_in_c[clas]:
			return 0

		return self.count_tk_in_c[clas][token]

	
	def probTokenGivenClass(self,token,clas):
		A = self.countTokenGivenClass(token,clas) + 1
		B = self.count_tk_in_c[class_]['___ALLTOKENS___']
		
		return A/float(B)

	def probTokenGivenClassSmoothing(self,token,clas):

		A = self.countTokenGivenClass(token,clas) + 1
		B = self.count_tk_in_c[class_]['___ALLTOKENS___'] + self.data_train.getVocabularySize()

		return A/float(B)

	def __str__(self):
		return 'Vocabulary size = %d\nNumber of classes = %d\n' % (self.getVocabularySize(),len(self.prior))

