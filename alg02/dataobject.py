class Dataobject(object):

	#@text_data is a dictionary: {'the':230
	def __init__(self,data,file_name,class_name='NA',class_score = 'NA',isCategorical=True):
		self.features = data.keys()
		self.class_name = class_name
		self.file_name = file_name
		self.isCategorical = isCategorical
		self.freq_tokens = data #{'the':230,'it':50...}
		self.class_score = class_score
		
	
	def getScore(self):
		
		if self.isCategorical:
			return self.getCategoricalScore()
		return self.class_score
	
	def getClass(self):
		return self.class_name
	
	def getFileName(self):
		return self.file_name.split('/')[-1]
	
	def getFeatures(self):
		return self.features
	
	def getCategoricalScore(self):
		return self.getClass()
	
	def getFreqTokens(self):
		return self.freq_tokens

	def removeToken(self,token):
		raise 'removeTOken(token) was not implemented'
	
	def removeStopWords(self,text):
		raise 'RemoveStopWords(text) was not implemented'
# 		stopwords = open('stop_words_review.stop').read()
# 		stopwords = stopwords.split('\n')
# 
# 		if len(text) > 0:
# 			
# 			for sw in stopwords:
# 			
# 				if sw in text:
# 					jtext = ' '.join(text)
# 					jtext = jtext.replace(' '+sw+' ',' ')
# 					text = jtext.split()
# 		return text