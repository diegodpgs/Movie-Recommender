import sys
import os
import time
import random
from datatext import *
from bayes import *

# def runCV(data_train,data_test):
# 	data = data_train.getMappedData()
# 	data.extend(data_test.getMappedData())
# 	random.shuffle(data)
	


if "__main__":
	TYPE_DATAS = ['review','srt','tags']
	movies = {}
	
	for TYPE_DATA in TYPE_DATAS:
		PATH_TRAIN = '/Users/happyhour/Documents/Recomender/data/train/parsed/'+TYPE_DATA+'/all'
		PATH_TEST  = '/Users/happyhour/Documents/Recomender/data/test/parsed/'+TYPE_DATA+'/all_data/all'
	
		data_train = DataText(TYPE_DATA,PATH_TRAIN)
		data_test  = DataText(TYPE_DATA,PATH_TEST)
	
		timetrain = time.time()
		NV = NaiveBayes(data_train,data_test)
		NV.train()
		#print 'RuntimeTrain: %1.2f' % (time.time()-timetrain)
		#print 'totalcount %d' % NV.totalcount
		#print '='*80
		
		for d in data_test.getSamples():
			file_name = d.getFileName().split('.')[0]
			if file_name not in movies:

				movies[file_name] = {'srt':None,'review':None,'tags':None,'score':0}
			result = NV.test_one(d)
			movies[file_name][TYPE_DATA] = NV.test_one(d)
			if result[-1] == 'yes_8_10':
				movies[file_name]['score'] += 1
	
	results = [(data['score'],movie,data)for movie,data in movies.iteritems()]
	results.sort()
	results = results[::-1]
	
	for movie in results:
		score = movie[0]
		name = movie[1]
		maximum = max([movie[-1]['srt'][0],movie[-1]['review'][0],movie[-1]['tags'][0]])

		print '%d %s %f' % (score,name,maximum)
# 		type_data = movie[-1]
# 		score = movie[0]
# 		name = movie[1]
# 
# 		print '%s SCORE: %d \n srt:%s\n review:%s\n tags:%s\n' % (name,score,type_data['srt'],type_data['review'],type_data['tags'])
	
