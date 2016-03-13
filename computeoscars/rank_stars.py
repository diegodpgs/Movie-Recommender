#coding: UTF-8
import urllib2
from oscars import *
import sys

"""
   README
   
   1 - Copy html code of watched list to a text file
   2 - Run the getMovies method
   3 - After the file top_movies_code_rank been written, run the method getCast
   
"""

def getMovies():
	list_page	= open('list_movies.txt').readlines()#urllib2.urlopen(list_url).readlines()
	movies = []
	
	for index in xrange(len(list_page)):
		line = list_page[index]
		#print '|your|' in line
		
		if '|your|' in line:
			#print line

			myscore = line.split('|your|')[1].split('|')[0]
			index_copy = index-1

			while index_copy > 0 and '/title/' not in list_page[index_copy]:
				index_copy -= 1
			
			movie_code = list_page[index_copy].split('href="/title/')[1].split('"')[0]
			movies.append((movie_code,myscore))
	
	movies_file = open('top_movies_code_rank.txt','w')
	for movie in movies:
		movies_file.write('%s;%s\n'% (movie[0],movie[1]))

def getCast(movie_url):
	cast = []

	movie_page	= urllib2.urlopen(movie_url).readlines()
	
	for index in xrange(5,len(movie_page)):
		
		if '<h1 class="header">' not in movie_page[index] and '/company/' not in movie_page[index-1]:
			if '<span class="itemprop" itemprop="name">' in movie_page[index]:
				name = movie_page[index].split('<span class="itemprop" itemprop="name">')[1].split('<')[0]
			
				if name not in cast:
					cast.append(name)
				
	return cast

movies = open('top_movies_code_rank.txt').read()
movies = movies.split('\n')
cast_scores = {}
count = 0

for movie in movies:
	count += 1.0
	codemovie = movie.split(';')[0]
	score = float(movie.split(';')[1])
	
	cast = getCast('http://www.imdb.com/title/%s/' % codemovie)
	
	for c in cast:
		if c not in cast_scores:
			cast_scores[c] = []
		
		cast_scores[c].append(score)
	
	print '%1.1f%% Processed' % ((count/len(movies))*100)


file_cast_score = open('my_stars.txt','w')

for star, scores in cast_scores.iteritems():
	file_cast_score.write('%s;%1.2f;%d\n' % (star,sum(scores)/len(scores),len(scores)))
	



# 			
# 		
# 		