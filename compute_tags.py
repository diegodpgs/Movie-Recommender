import urllib2
import os

def writeTags(PATH_input,PATH_output):
	
	for movie_file_name in os.listdir(PATH_input):
		file_tags_category = open('%s/%s.tags' % (PATH_output,movie_file_name.split('.')[0]),'w')
		PATH_output_join_all = PATH_output.split('category')[0]+'all/'+PATH_output.split('category')[1].split('/')[1]
		file_tags_all = open('%s/%s.tags' % (PATH_output_join_all,movie_file_name.split('.')[0]),'w')
		if 'DS_Store' not in movie_file_name:
			tags = getTags(movie_file_name.split('_')[-1].split('.srt')[0])
		
			for key,values in tags.iteritems():
				file_tags_category.write('%s;#;%d;#;%d\n' % (key,values[0],values[1]))
				file_tags_all.write('%s;#;%d;#;%d\n' % (key,values[0],values[1]))
				
				
def getTags(title_code): 	
						
	link = urllib2.urlopen('http://www.imdb.com/title/%s/keywords' % title_code).readlines()
	tags = {}
	
	
	for index in xrange(500,len(link)):
		line = link[index]
	
		if 'this relevant' in line:
			out = 0
			total = 0
		
			if 'found' in line:
				out =  int(line.split('of')[0].split('>')[1])
				total = int(line.split('of')[1].split('found')[0])
		

			word = link[index-5].split('</a>')[0].split('>')[1]
			word = word.replace(' ','_')
			tags[word] = (out,total)
	
	return tags
				
		



PATH_input = os.getcwd()+'/data/original_data/SRT/'
PATH_output = os.getcwd()+'/data/original_data/tags/'

if '.DS_Store' in os.listdir(PATH_input+'category'):
	os.remove(PATH_input+'category/.DS_Store')
	
for classe in os.listdir(PATH_input+'category'):
	if classe not in os.listdir(PATH_output+'category'):
		os.mkdir(PATH_output+'category/%s' % classe)
		os.mkdir(PATH_output+'all/%s' % classe)

	if '.DS_Store' in os.listdir(PATH_input+'category/%s' % classe):
			os.remove(PATH_input+'category/%s/.DS_Store' % classe)
	

	for folder in os.listdir(PATH_input+'category/%s' % classe)[5:]:
			if folder not in os.listdir(PATH_output+'category/%s' % classe):
				os.mkdir(PATH_output+'category/%s/%s' % (classe,folder))
		
			writeTags(PATH_input+'category/%s/%s' % (classe,folder),
						PATH_output+'category/%s/%s' % (classe,folder)) 	