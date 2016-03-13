from bayes import *



def test(PATH_train, PATH_test, threshold):
	movies = {}
	movies_results = {}

	
	for i in xrange(5):
		results = getResults(PATH_train,PATH_test)
	
		for r in results:
			if r[1] not in movies:
				movies[r[1]] = []
		
			movies[r[1]].append(r[0])
		
		print '%1.2f processed' % ((i+1)/5.)
	
	for movie,results in movies.iteritems():
		movies_results[movie] = (sum(results)/len(results),[r > threshold for r in results].count(True))
	

	return movies_results

def showFinalResults():
# 	print '-'*40
# 	print '-'*17,'SRT','-'*17
# 	srt = test('/Users/happyhour/Documents/Recomender/data/parsed_data/SRT/all/',
# 	'/Users/happyhour/Documents/Recomender/data/parsed_data_new/SRT/all/',
# 	.7)
# 
# 	
# 	for name,results in srt.iteritems():
# 		print '%s %1.2f %d' % (name,results[0],results[1])
# 		
# 	#-----------------------------------------------------------------------
# 	print '-'*40
# 	print '-'*17,'Tags','-'*17
# 	tags = test('/Users/happyhour/Documents/Recomender/data/parsed_data/tags/all/',
# 	'/Users/happyhour/Documents/Recomender/data/parsed_data_new/tags/all/',
# 	.6)
# 
# 	
# 	for name,results in tags.iteritems():
# 		print '%s %1.2f %d' % (name,results[0],results[1])
# 	
	#-----------------------------------------------------------------------
	print '-'*40
	print '-'*17,'Reviews','-'*17
	tags = test('/Users/happyhour/Documents/Recomender/data/parsed_data/Review/all/',
	'/Users/happyhour/Documents/Recomender/data/parsed_data_new/Review/all/',
	.8)

	
	for name,results in tags.iteritems():
		print '%s %1.2f %d' % (name,results[0],results[1])
		

if "__main__":
	showFinalResults()
	
	
		
		