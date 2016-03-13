import urllib2
import os

CACHE_TAGS = {}
def writeTags(PATH_input,PATH_output):

	#print PATH_output
	PATH_output_join_all = PATH_output.split('category')[0]+'all/'+PATH_output.split('category')[1].split('/')[1]	

	for movie_file_name in os.listdir(PATH_input):
	
		file_name = movie_file_name.split('.')[0]
		file_tags_category = open('%s/%s.tags' % (PATH_output,file_name),'w')
		file_tags_all = open('%s/%s.tags' % (PATH_output_join_all,file_name),'w')
		
		if 'DS_Store' not in movie_file_name:
			tags = getTags(movie_file_name.split('_')[-1].split('.srt')[0])
		
			for key,values in tags.iteritems():
				file_tags_category.write('%s;#;%d;#;%d\n' % (key,values[0],values[1]))
				file_tags_all.write('%s;#;%d;#;%d\n' % (key,values[0],values[1]))
				
def getTags(title_code): 	
			
	if title_code in CACHE_TAGS:
		print 'returned'
		return CACHE_TAGS[title_code]
					
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
	
	CACHE_TAGS[title_code] = tags
	return tags
						
def run(PATH_input,PATH_output):

	if '.DS_Store' in os.listdir(PATH_input):
		os.remove(PATH_input+'.DS_Store')
	
	for classe in os.listdir(PATH_input):
		if classe not in os.listdir(PATH_output+'category'):
			os.mkdir(PATH_output+'category/%s' % classe)
			os.mkdir(PATH_output+'all/%s' % classe)

		if '.DS_Store' in os.listdir(PATH_input+'%s' % classe):
				os.remove(PATH_input+'%s/.DS_Store' % classe)
	

		for folder in os.listdir(PATH_input+'%s' % classe):
				if folder not in os.listdir(PATH_output+'category/%s' % classe):
					os.mkdir(PATH_output+'category/%s/%s' % (classe,folder))
		
				writeTags(PATH_input+'%s/%s' % (classe,folder),
							PATH_output+'category/%s/%s' % (classe,folder)) 	


if "__main__":
	PATH_input = os.getcwd()+'/data/test/original/SRT/new/category/'
	PATH_output = os.getcwd()+'/data/test/original/tags/new/'
	
	run(PATH_input,PATH_output)
