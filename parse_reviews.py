import os
import nltk
from sequences import *
from utils import *
from parser import *

computed_movies = ['.DS_Store']

def normalizeReviews(text_data):
	new_text_data  = ''
	#1;#;281;#;342;#;I had my doubts. I knew that Pixar would fail this time around. No way were they going to pull this off for a seventh time.  I was very, very wrong.  I went to see a special screening of "Cars" a few weeks ago, and this movie blew me away. The animation is gorgeous, the story brings a smile to your face, and you can't help falling in love with all of the colorful characters. It definitely has that genuine Pixar "heart" that you rarely see in any other CGI film. At first I thought the movie would be centered around a lot of NASCAR-like racing, but it really wasn't, much to my surprise (and pleasure). This movie is definite Pixar gold. I absolutely loved it.  Although I don't want to give any spoilers away, I will say that my favorite scene would have to be when Mater drags McQueen out to do a bit of "Tractor Tipping". The whole theater was filled with laughter. Heck, it even got some laughs out of me, which is rare when it comes to a kid's movie.  Be there on opening night. This is movie is worth all of your time and mone
	for review in text_data:
			
		if ';#;' in review:
			out = int(review.split(';#;')[1])
			total = float(review.split(';#;')[2])
			
			if (out/total) > .6 and out > 2:
				new_text_data += review.split(';#;')[3]
			
	return tokenize(new_text_data,'')
	
def parseReview(PATH_input,PATH_output):
	all_tokens = []
	movies_tokens = {}
	
	
	for movie_file_name in os.listdir(PATH_input):

		if 'DS_Store' not in movie_file_name:
			data = open(PATH_input+'/'+movie_file_name).readlines()
			review_tokens = normalizeReviews(data)
		
			if movie_file_name not in computed_movies:
				computed_movies.append(movie_file_name)
				all_tokens.extend(set(review_tokens))
			
			movies_tokens[movie_file_name] = review_tokens
			
			print '%s parsed' % movie_file_name
	
	return {'all_tokens':all_tokens,'movies_tokens':movies_tokens}


def run(PATH_input, PATH_output,file_vocabulary=None):

	srt_data = {}
	if '.DS_Store' in os.listdir(PATH_input+'/category'):
		os.remove(PATH_input+'/category/.DS_Store')
	
	all_tokens = []
	
	for classe in os.listdir(PATH_input+'/category'):
		srt_data[classe] = {}
		if classe not in os.listdir(PATH_output+'/category'):
			os.mkdir(PATH_output+'/category/%s' % classe)
			os.mkdir(PATH_output+'/all/%s' % classe)
		
		
	
		if '.DS_Store' in os.listdir(PATH_input+'/category/%s' % classe):
			os.remove(PATH_input+'/category/%s/.DS_Store' % classe)
	
		for genre in os.listdir(PATH_input+'/category/%s' % classe):
			
			if genre not in os.listdir(PATH_output+'/category/%s' % classe):
				os.mkdir(PATH_output+'/category/%s/%s' % (classe,genre))
			
				
			result = parseReview(PATH_input+'/category/%s/%s' % (classe,genre),PATH_output+'category/%s/%s' % (classe,genre))
			all_tokens.extend(result['all_tokens'])
			srt_data[classe][genre] = result['movies_tokens']
	
	if file_vocabulary == None:
		srt_data = applyThreshold(srt_data,nltk.FreqDist(all_tokens))
	else:
		data_vocabulary = open(file_vocabulary).read().split('\n')
		srt_data = applyThreshold(srt_data,nltk.FreqDist(all_tokens),data_vocabulary)
	
	writeData(PATH_output,srt_data)
		
if "__main__":
	PATH_input =  os.getcwd()+'/data/test/original/Review/new/'
	PATH_output = os.getcwd()+'/data/test/parsed/Review/new'
	run(PATH_input,PATH_output,'vocabulary_review.voc')