import os
import sys
from utils import *
from parser import *

computed_movies = ['.DS_Store']
def parseTags(PATH_input,PATH_output):
	
	total_tokens = []
	movies_tags = {}
	
	for movie_file_name in os.listdir(PATH_input):
	
		
		if 'DS_Store' not in movie_file_name:
			keywords = open(PATH_input+'/'+movie_file_name).read()
			keywords = keywords.split('\n')
			tags_tokens = []
			
			#if movie_file_name not in computed_movies:
			for keyword_data in keywords[0:-1]:
				keyword = keyword_data.split(';#;')[0]
				out = float(keyword_data.split(';#;')[1])
				total = float(keyword_data.split(';#;')[2])
				
				
				if total == 0:
					tags_tokens.append((1,keyword))
					
				elif out == 0:
					tags_tokens.append((2,keyword))
			
				elif out < total:
					tags_tokens.append((3,keyword))
			
				else:
					tags_tokens.append((4,keyword))
			
				total_tokens.append(keyword)
				
			computed_movies.append(movie_file_name)
			tags_tokens.sort()
			movies_tags[movie_file_name] = tags_tokens[::-1]
			
			print '%s parsed' % movie_file_name
	
	return {'all_tokens':total_tokens,'movies_tokens':movies_tags}

def run(PATH_input, PATH_output):

	tags_data = {}
	if '.DS_Store' in os.listdir(PATH_input+'/category'):
		os.remove(PATH_input+'/category/.DS_Store')
	
	all_tokens = []
	
	for classe in os.listdir(PATH_input+'/category'):
		tags_data[classe] = {}
		if classe not in os.listdir(PATH_output+'/category'):
			os.mkdir(PATH_output+'/category/%s' % classe)
			os.mkdir(PATH_output+'/all/%s' % classe)
		
		
	
		if '.DS_Store' in os.listdir(PATH_input+'/category/%s' % classe):
			os.remove(PATH_input+'/category/%s/.DS_Store' % classe)
	
		for genre in os.listdir(PATH_input+'/category/%s' % classe):
			
			if genre not in os.listdir(PATH_output+'/category/%s' % classe):
				os.mkdir(PATH_output+'/category/%s/%s' % (classe,genre))
				
			result = parseTags(PATH_input+'/category/%s/%s' % (classe,genre),PATH_output+'category/%s/%s' % (classe,genre))
			all_tokens.extend(result['all_tokens'])
			tags_data[classe][genre] = result['movies_tokens']
	
	
	writeData(PATH_output,tags_data)

if "__main__":
	PATH_input =  os.getcwd()+'/data/test/original/tags/new'
	PATH_output = os.getcwd()+'/data/test/parsed/tags/new'
	run(PATH_input,PATH_output)