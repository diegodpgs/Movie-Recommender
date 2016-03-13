#coding: UTF-8
import urllib2
import os

"""
	@author Diego Pedro
	
	This code get data from imdb of reviews and write in a specific file
	for each movie
	
"""

CACHE_REVIEWS = {}
def cleanReview(review):
	review = review.replace('\n',' ')
	
	for tag in ['<br>','</br>']:
		review = review.replace(tag,' ')
	
	unicode = [('&#x27;',"'"),('&#x96;','-'),('&#x22;','"'),('\n',' '),('&#39;',"'"),('&quot;','"')]
	
	for uni in unicode:
		review = review.replace(uni[0],uni[1])
	
	return review[0:-3]

def processReviews(reviews_page):
	reviews = []
	review = ''
	review_found = False
	score = 0
	

	for line in reviews_page[500:]: #start from 500 because the previous html code are unseful

		
		if 'people found the following review useful' in line:

			out =  int(line.split('out of')[0].split('>')[1])
			total = int(line.split('people')[0].split('of')[1])
			review_found = True
			review += '%d;#;%d;#;' % (out,total)
			
			
		if review_found and line[0] != '<':
			
			if '\n' != line and len(line) >= 5:
				review += line
				review = review.replace('\n',' ')
				
		
		if '</p>' in line and review_found:
			review_found = False
			
			
			if len(review) > 50:
				reviews.append(cleanReview(review))
			review = ''
	
	return reviews

def getReviews(title_code,file_name,pages=1):

	if title_code in CACHE_REVIEWS:
		print 'FROM CACHE'
		return CACHE_REVIEWS[title_code]
		
	reviews_page = urllib2.urlopen("http://www.imdb.com/title/%s/reviews" % title_code).readlines()
	reviews = processReviews(reviews_page)
	
	if pages > 1:
	
		for page in xrange(1,pages):
			try:
				reviews_page = urllib2.urlopen("http://www.imdb.com/title/%s/reviews?start=%d" % (title_code,page*10)).readlines()
				reviews.extend(processReviews(reviews_page))
			except:
				print 'The movie of title %s has less than %d pages' % (title_code,page)
	  
	
 	
	
	print '%d reviews processed of %s' % (len(reviews),file_name)
	CACHE_REVIEWS[title_code] = reviews
	return reviews
	
def writeReview(PATH_input,PATH_output,pages=1):

	PATH_output_join_all = PATH_output.split('category')[0]+'all/'+PATH_output.split('category')[1].split('/')[1]
	for movie_file_name in os.listdir(PATH_input):

		file_name = movie_file_name.split('.')[0]
		file_review_category = open('%s/%s.review' % (PATH_output,file_name),'w')
		file_review_all = open('%s/%s.review' % (PATH_output_join_all,file_name),'w')
		
		if 'DS_Store' not in movie_file_name:
			reviews = getReviews(movie_file_name.split('_')[-1].split('.srt')[0],file_name,pages)
		
			for index in xrange(len(reviews)):
				review = reviews[index]
				file_review_category.write('%d;#;%s\n' % (index+1,review))
				file_review_all.write('%d;#;%s\n' % (index+1,review))
			

def run(PATH_input,PATH_output,pages=1):

	if '.DS_Store' in os.listdir(PATH_input+'category'):
		os.remove(PATH_input+'category/.DS_Store')
	
	for classe in os.listdir(PATH_input+'category'):
		if classe not in os.listdir(PATH_output+'category'):
			os.mkdir(PATH_output+'category/%s' % classe)
			os.mkdir(PATH_output+'all/%s' % classe)

		if '.DS_Store' in os.listdir(PATH_input+'category/%s' % classe):
				os.remove(PATH_input+'category/%s/.DS_Store' % classe)
	

		for folder in os.listdir(PATH_input+'category/%s' % classe)[7:]:
				if folder not in os.listdir(PATH_output+'category/%s' % classe):
					os.mkdir(PATH_output+'category/%s/%s' % (classe,folder))
		
				writeReview(PATH_input+'category/%s/%s' % (classe,folder),
							PATH_output+'category/%s/%s' % (classe,folder),pages) 	
			

if "__main__":
	
	PATH_input = os.getcwd()+'/data/test/original/SRT/new/'
	PATH_output = os.getcwd()+'/data/test/original/Review/new/'
	
	run(PATH_input,PATH_output,4)
					
