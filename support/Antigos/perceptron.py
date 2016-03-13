import math
class Perceptron:

	"""
		DATA FORMAT
		
		data = [[xa1,xa2,xa3,xa4...xan,ay],
				[xb1,xb2,xb3,xb4...xbn,by],
						.
						.
						.
				[xz1,xz2,xz3,xz4...xzn,zy]]
		
		where xn is a feature and y is the target expected. 
			  Both have to be numeric.
			
		
		
	"""
	def __init__(self,data):
		self.data = data
		self.targets   = [x[-1]   for x in data]
		self.features = [x[0:-1] for x in data]
		self.weights = None
		self.bias = None
		
	
	def updateWeights(self,X,y):
	
		for feature in xrange(len(X)):
			self.weights[feature] += (y * X[feature]) 
			
	#@max_interaction the value of interactions
	def train(self,max_interaction):
		M = len(self.features[0]) #number of features
		N = len(self.data) # number of train samples
		self.weights = [0 for i in xrange(M)]
		self.bias = 0 #bias


		for i in xrange(max_interaction):
		
			for index in xrange(N):
			
				y = self.predict(self.features[index])

				
				if y != self.targets[index]:

					self.updateWeights(self.features[index],self.targets[index])
					self.bias = self.bias + y
			print 'WEIGHTS',self.weights
					

	#@X : sample test X = [x1,x2..xn]
	def predict(self,X):
		N = len(X) #number of features

		score = sum([self.weights[j]*X[j] for j in xrange(N)]) + self.bias

		if score >= 0:
			return 1
			
		return -1

# if "__main__":
# 
# 	data = [(0,1,-1),(1,0,-1),(0,0,1),(1,1,1)]
# 	
# 	p = Perceptron(data)
# 	p.train(10)
# 
# 	#peking, shangai, shangai, tokyo, tshishuan, yokohama:c
# 	#peking, osaka, shangai, tokyo, kyoto, yokohama:j
# 	#baidu, shangai, peking, kyoto, tshishuan, yokohama:c
# 	#osaka, osaka, shangai, yoto, osaka:j
# 	#peking, peking, peking, osaka, osaka:c
# 	#yokohama, kyoto, shangai, baidu tshishuan:c
# 	#----
# 	#osaka, baidu, baidu, baidu, osaka:c
# 	#kyoto, osaka, osaka, kyoto, peking:j
# 
# 	#peking, baidu, shangai, tokyo,tshishuan, yokohama,osaka,kyoto
# 
# 	# data = [(1, 0, 2, 1, 1, 1, 0, 0, 1),
# # 			(1, 0, 1, 1, 0, 1, 1, 1, -1),
# # 			(1, 1, 1, 0, 1, 1, 0, 1, 1),
# # 			(0, 0, 1, 0, 0, 0, 3, 0, -1),
# # 			(3, 0, 0, 0, 0, 0, 2, 0, 1),
# # 			(0, 1, 1, 0, 1, 1, 1, 1, 1)]
# # 
# # 	testX = [(0, 3, 0, 0, 0, 0, 1, 1),
# # 			(1, 0, 0, 0, 0, 0, 2, 2)]
# # 			
# # 	testY = [1,-1]
# 
