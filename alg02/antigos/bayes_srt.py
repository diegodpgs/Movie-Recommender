import os
import random
import nltk
import math
import time
from bayes import NaiveBayes
from sklearn import metrics
from sequences import *

class Dataobject(object):

	#@text_data is a string
	
	def __init__(self,text_data,file_name,class_score='NA',class_name='NA',isCategorical=True):
		text_data.replace('\n','')
		self.tokens = self.tokenize(text_data)
		self.class_score = class_score
		self.class_name = class_name
		self.file_name = file_name
		self.isCategorical = isCategorical
		
		#storage the frequency of tokens token: frequency
		self.features_map = self.calculateFeaturesTable() 
	
		
	def tokenize(self,data_raw,lower=True):
		data_raw = data_raw.split('\n')
		return data_raw
	
	def calculateFeaturesTable(self):
		tokens_dic = {}
		
		for token in self.tokens[0:-1]:
			tok = token.split()[0]
			freq = int(token.split()[1])
			tokens_dic[tok] = freq
		
		return tokens_dic
		
	
	def getScore(self):
		
		if self.isCategorical:
			return self.getCategoricalScore()
		return self.class_score
	
	def getClass(self):
		return self.class_name
	
	def getFileName(self):
		return self.file_name.split('/')[-1]
	
	def getFeatures(self):
		return set(self.tokens)
	
	def getCategoricalScore(self):
		return self.getClass()
	
	def getFeaturesMap(self):
		return self.features_map
						
	
	def removeStopWords(self,text):
		print 'ANTES'
		t = time.time()
		stopwords = open('stop_words_srt.stop').read()
		stopwords = stopwords.split('\n')

		if len(text) > 0:
			
			for sw in stopwords:
			
				if sw in text:
					jtext = ' '.join(text)
					jtext = jtext.replace(' '+sw+' ',' ')
					text = jtext.split()
		print 'DEPOIS',time.time()-t
		return text
	

#@classes a dict X:Y where X is the name of the folder in the path 
#					   and Y is the respective value assigned to that class
#				
def readData(PATH,classes):
	data = []
	total_files = 207.0
	count = 0
	
	total_data = []

	for classe in classes:
		
		for file_name in os.listdir(PATH+classe):
			if '.DS_Store' in file_name:
				continue

			count += 1
			text_data = open(PATH+classe+'/'+file_name).read()
			#print 'openning files.... %1.2f%% concluded' % ((count/total_files)*100)
			d = Dataobject(text_data,file_name,classes[classe],classe)
			#print d.tokens
			
			data.append(d)
	return data

def getCVfolders(data,folders_q=5):
	random.shuffle(data)
	data_copy = data[:]
	folders = [[] for i in xrange(folders_q)]
	folder_index = 0
	
	while len(data_copy) > 0:
		sample_index = random.randint(0,len(data_copy)-1)
		folders[folder_index % folders_q].append(data_copy[sample_index])
		
		del data_copy[sample_index]
		folder_index += 1
	
	return folders
			
def runCV(folders, new_data):
	
	# results = {'Accuracy':[],'Precision':[],'Recall':[],'F1':[]}
# 	results_AVG = {'Accuracy':[],'Precision':[],'Recall':[],'F1':[]}
	results = {}
	
	for index in xrange(len(folders)):
		test = folders[index]
		train = []
		
		for index2 in xrange(len(folders)):
			if index2 != index:
				train.extend(folders[index2])	
		
		NV = NaiveBayes(train,test,False)
		NV.train()
		
		for sample in new_data:
			result_class = NV.test_one(sample)
			
			if sample.file_name not in results:
				results[sample.file_name] = {}
			
			if result_class not in results[sample.file_name]:
				results[sample.file_name][result_class] = 0
			
			results[sample.file_name][result_class] += 1
		
# 		result = NV.test()
# 		for metric,value in result.iteritems():
# 			results[metric].append(value)
		
# 	for metric, values in results.iteritems():
# 		results_AVG[metric] = sum(values)/len(values)

# 	return (results_AVG,results_tests)

	return results
		
def getResults(PATH_train,PATH_test):

	data = []
	samples_test = []
	classes_train = os.listdir(PATH_train)
	classes_test = os.listdir(PATH_test)
	
	if '.DS_Store' in classes_train:
		classes_train.remove('.DS_Store')
		
	if len(classes_train) == 2:
		data = readData(PATH_train,{classes_train[0]:-1,classes_train[1]:1})
		samples_test = readData(PATH_test,{classes_test[0]:-1,classes_test[1]:1})
	else:
		classes = {}
		
		for index in xrange(len(classes_train)):
			classes[classe_train[index]] = index + 1
		
		data = readData(PATH_train,classes)
		samples_test = readData(PATH_test,classes)
	foldersCV = getCVfolders(data)
	
	results_sample_test = runCV(foldersCV,samples_test)
	
	results_normalized = []
	
	for file_name,result in results_sample_test.iteritems():
		if len(result.keys()) == 2:
			results_normalized.append((result['yes_8_10']/float(result['yes_8_10']+result['no_1_7']),file_name))
		elif 'yes_8_10' in result:
			results_normalized.append((1.0,file_name))
		else:
			results_normalized.append((0.0,file_name))
	
	
	return results_normalized
	
	
			

	
	
# if "__main__":
# 	
# 	PATH_train = '/Users/happyhour/Documents/Recomender/data/parsed_data/SRT/all/'
# 	PATH_test  = '/Users/happyhour/Documents/Recomender/data/parsed_data_new/SRT/all/'
# 	getResults(PATH_train,PATH_test)