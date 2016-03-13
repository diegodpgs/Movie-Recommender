import os
import random
import nltk
import math
from bayes import NaiveBayes
from sklearn import metrics
from sequences import *


class Dataobject(object):

	#@text_data is a string
	
	def __init__(self,text_data,file_name,class_score='NA',class_name='NA',isCategorical=True):
		#text_data.replace('\n','')
		self.tokens = text_data
		
		self.class_score = class_score
		self.class_name = class_name
		self.file_name = file_name
		self.isCategorical = isCategorical
		
		#storage the frequency of tokens token: frequency
		self.features_map = self.calculateFeaturesTable() 
	
	def addBigrams(self,data):
		bigram = getBigram(data)[1]
		return bigram
		
		
	def tokenize(self,data_raw,lower=True):
		punct = list('.,:;!')
		#print data_raw
	
		if lower:
			data_raw = data_raw.lower()
	
		for p in punct:
			#data_raw = data_raw.replace(p,' %s ' % p)
			data_raw = data_raw.replace(p,' ')
		
		
		data_raw = data_raw.split()
		bigrams = self.addBigrams(data_raw)
		new_data = []
		try:
			tokens_tag = nltk.pos_tag(data_raw)
		
			for tt in tokens_tag:
				if tt[1] == 'NN':
					new_data.append(tt[0])
		except:
			print 'exception'
			new_data = data_raw[:]
		
		new_data.extend(bigrams)
		
		return self.removeStopWords(new_data)
	
	def calculateFeaturesTable(self):
	
		frequencies = nltk.FreqDist(self.tokens)
		return dict(frequencies.iteritems())
		
	
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

	def removeToken(self,token):
		if token in self.tokens:
			jtext = ' '.join(self.tokens)
			jtext = jtext.replace(' '+token+' ',' ')
			self.tokens = jtext.split()
	
	def removeStopWords(self,text):
		stopwords = open('stop_words_review.stop').read()
		stopwords = stopwords.split('\n')

		if len(text) > 0:
			
			for sw in stopwords:
			
				if sw in text:
					jtext = ' '.join(text)
					jtext = jtext.replace(' '+sw+' ',' ')
					text = jtext.split()
		return text
	
def removeTokens(data,tokens_set,count=1):
	ft = nltk.FreqDist(tokens_set)
	fdist = zip(ft.values(),ft.keys())
	fdist.sort()
	
	index = 0
	removed = 0
	while fdist[index][0] <= count:
		for d in data:
			d.removeToken(fdist[index][1])
		
		removed += 1	
		
		index += 1
		print fdist[index]
	print '%d tokens removed' % removed
	return data
		

#@classes a dict X:Y where X is the name of the folder in the path 
#					   and Y is the respective value assigned to that class
#				
def readData(PATH,classes):
	data = []
	total_files = 206.0
	count = 1
	
	total_data = []

	for folder in classes:
		
		for file_name in os.listdir(PATH+folder):
			if '.DS_Store' in file_name:
				continue
			count += 1
			text_data = open(PATH+folder+'/'+file_name).read()
			
			#print 'openning files.... %1.2f%% concluded' % ((count/total_files)*100)
			d = Dataobject(text_data.split(),file_name,classes[folder],folder)
			#print d.tokens
			
			data.append(d)
			total_data.extend(set(d.tokens))
	
	
	
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
		
def parseReviews(text_data):
	new_text_data  = ''
	
	for review in text_data:
			
		if ';#;' in review:
			new_text_data += review.split(';#;')[1]
	
	return new_text_data
	
def runCV(folders,test_sample):
	
	results = {'Accuracy':[],'Precision':[],'Recall':[],'F1':[]}
	results_AVG = {'Accuracy':[],'Precision':[],'Recall':[],'F1':[]}
	
	results_tests = {'yes_8_10':0,'no_1_7':0}
	
	for index in xrange(len(folders)):
		test = folders[index]
		train = []
		
		for index2 in xrange(len(folders)):
			if index2 != index:
				train.extend(folders[index2])	
		
		NV = NaiveBayes(train,test,False)
		NV.train()
		result = NV.test()
		results_tests[NV.test_one(test_sample)] += 1
		
		for metric,value in result.iteritems():
			results[metric].append(value)
		
	for metric, values in results.iteritems():
		results_AVG[metric] = sum(values)/len(values)

	return (results_AVG,results_tests)
		
	
if "__main__":
	PATH = '/Users/happyhour/Documents/Recomender/data/parsed_data/Review/'
	folders = os.listdir(PATH)
	folders.sort()
	files = []
	
	for f in folders[1:-2]:
	
		files.append(os.listdir(PATH+f)[2])
	results_files = []
	
	for index in xrange(1,len(folders)-2):
		
		results = {'Accuracy':[],'Precision':[],'Recall':[],'F1':[]}
		veredito = {'yes_8_10':0,'no_1_7':0}
		data = readData('/Users/happyhour/Documents/Recomender/data/parsed_data/Review/%s/' % folders[index],{'no_1_7':-1.0,'yes_8_10':1.0})
	
		peformance = []
		peformance_sample = []
	
		for i in xrange(3):
			foldersCV = getCVfolders(data)
		
			test_sample = open('/Users/happyhour/Documents/Recomender/data/parsed_data/Review/%s/%s' % (folders[index],files[index-1])).read()
			sample_data = Dataobject(test_sample.split(),'50_dates',1.0,'yes_8_10')
		
			result_test,result_sample_test = runCV(foldersCV,sample_data)
			peformance_sample.append((float(result_sample_test['yes_8_10'])/sum(result_sample_test.values())))
			peformance.append(result_test['Precision'])
			#print '       CV %d processed' % (i+1)


		#print 'Final Performance : %1.3f' % (sum(peformance)/len(peformance))
		results_files.append((files[index-1],'%1.3f' % (sum(peformance_sample)/len(peformance_sample))))
		print  files[index-1]
		#print 'Final Performance Sample: %1.3f' % ()
	results_files.sort()
	for r in results_files:
		print '%s %s' % (r[0],r[1])
	
# Discovere what is the problem with high precision for test one using reviews
# review the precision calculus

	
		
