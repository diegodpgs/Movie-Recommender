import sys
import os
import time
from dataobject import *
"""
	For trainning and the test must to read just one folder
	
"""

class DataText:

	def __init__(self,type_data,path):
		self.type_data = type_data
		self.path = path
		self.samples = [] #a list of dataobject 
		self.vocabulary = None
		self.classes = None
		self.target_mapped = None
		self.processData()


	def processData(self):
		rawdata = self.readData()
		vocabulary = []
		classes = set()
		targets = {}
		for d in rawdata:
			
			if '.%s' % self.type_data == d.getFileName():
				continue
				
			self.samples.append(d)
			vocabulary.extend(d.getFeatures())
			classes.add(d.getClass())
			targets[d.getFileName()] = d.getScore()
			

		self.vocabulary = list(set(vocabulary))
		self.classes = classes
		self.target_mapped = targets

		
	def parseData(self,text_data):
		file_data = text_data.split('\n')
	
		data = [(sample.split()[0],int(sample.split()[1])) for sample in file_data[:-1]]
	
		return dict(data)
	
	#@classes a dict X:Y where X is the name of the folder in the path 
	#					   and Y is the respective value assigned to that class
	#				
	def readData(self):
		data = []
		starttime = time.time()
		#for each type of class
		# binary: yes, no
		# multiclass: bad, regular, good
		# numeric: '1', '2', '3'...'10'
		for classtype in os.listdir(self.path):
			if '.DS_Store' in classtype:
				os.remove(self.path+'/.DS_Store')
				continue
			
			listofiles = os.listdir(self.path+'/'+classtype)
			filesbyclass = len(listofiles)
			filescomputed = 0
			
			
			#list all files: srt, 
			for file_name in listofiles:
				if '.DS_Store' in file_name:
					os.remove(self.path+'/'+classtype+'/.DS_Store')
					continue
				
				filescomputed += 1.0
				text_data = open('%s/%s/%s' % (self.path,classtype,file_name)).read()
			
				#print 'openning files.... %1.2f%% concluded' % ((filescomputed/filesbyclass)*100)
				d = Dataobject(self.parseData(text_data),file_name,classtype)
				data.append(d)
			#print 'Class %s concluded\n%d samples processed\n' % (classtype,len(data))
	
		#print 'Data %s processed\nRuntime:%1.2f\n%s' % (self.path,time.time()-starttime,'-'*80)
		return data
			
	def getVocabulary(self):
		return self.vocabulary
	
	def getVocabularySize(self):
		return len(self.vocabulary)
	
	def getSamples(self):
		return self.samples
	
	def getClasses(self):
		return self.classes
	
	def getTargetMapped(self):
		return self.target_mapped



