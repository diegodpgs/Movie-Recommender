import os
import sys
from utils import *
from parser import *

computed_movies = ['.DS_Store']
def normalizeSRT(srt):
	srt_parsed = ''
	gaps = []
	
	
	for line in srt:
		line = line.replace('\n','')
		
		if '-->' in line:
			try:
				time1,time2 = counttime(line)
			except:
				print line
				raise 
			gaps.append((time1,time2))
		elif len(line) > 0 and line[0].isalpha():
			srt_parsed += line
	
	
	
	summary =  summaryGap(gaps)
	srt_parsed = tokenize(srt_parsed,'stop_words_srt.stop')
	
	return {'srt_parsed':srt_parsed,'summary':summary}
	
def parseSRT(PATH_input,PATH_output):
	
	total_tokens = []
	movies_srt = {}
	
	for movie_file_name in os.listdir(PATH_input):
	
		
		if 'DS_Store' not in movie_file_name:
			srt = open(PATH_input+'/'+movie_file_name).readlines()
			srt_tokens = normalizeSRT(srt)['srt_parsed']
			
			if movie_file_name not in computed_movies:
				computed_movies.append(movie_file_name)
				total_tokens.extend(set(srt_tokens))
			
			movies_srt[movie_file_name] = srt_tokens
			
			print '%s parsed' % movie_file_name
	
	return {'all_tokens':total_tokens,'movies_tokens':movies_srt}

def run(PATH_input, PATH_output,file_vocabulary=None):

	srt_data = {}
	if '.DS_Store' in os.listdir(PATH_input):
		os.remove(PATH_input+'/.DS_Store')
	
	all_tokens = []
	
	for classe in os.listdir(PATH_input):
		srt_data[classe] = {}
		if classe not in os.listdir(PATH_output+'/category'):
			os.mkdir(PATH_output+'/category/%s' % classe)
			os.mkdir(PATH_output+'/all/%s' % classe)
		
		
	
		if '.DS_Store' in os.listdir(PATH_input+'/%s' % classe):
			os.remove(PATH_input+'/%s/.DS_Store' % classe)
	
		for genre in os.listdir(PATH_input+'/%s' % classe):
			
			if genre not in os.listdir(PATH_output+'/category/%s' % classe):
				os.mkdir(PATH_output+'/category/%s/%s' % (classe,genre))
				
			result = parseSRT(PATH_input+'/%s/%s' % (classe,genre),PATH_output+'category/%s/%s' % (classe,genre))
			all_tokens.extend(result['all_tokens'])
			srt_data[classe][genre] = result['movies_tokens']
	
	if file_vocabulary == None:
		srt_data = applyThreshold(srt_data,nltk.FreqDist(all_tokens))
	else:
		data_vocabulary = open(file_vocabulary).read().split('\n')
		srt_data = applyThreshold(srt_data,nltk.FreqDist(all_tokens),data_vocabulary)
		
	writeData(PATH_output,srt_data)

if "__main__":
	PATH_input =  os.getcwd()+'/data/test/original/SRT/new/category'
	PATH_output = os.getcwd()+'/data/test/parsed/SRT/new'
	run(PATH_input,PATH_output,'vocabulary_srt.voc')