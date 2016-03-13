import sys
import os

# vocabulary_cache = open('vocabulary_srt_cache_1000.voc').read()
# vocabulary_cache = vocabulary_cache.split('\n')

def readVocabularyFile(file_name):
	v_file = open(file_name)
	v = v_file.readlines()
	v_file.close()

	vocabulary = {}


	for w in v:
		w = w.split()[0]
	
		if w not in vocabulary:
			vocabulary[w] = 0
		vocabulary[w] += 1
	
	return vocabulary

def increaseVocabulary(PATH_input,file_name):
	vocabulary = readVocabularyFile(file_name)
	v_file = open(file_name,'a')
	
	for classe in os.listdir(PATH_input):
		
		if '.DS_Store' not in classe:
		
			for f in os.listdir(PATH_input+'/'+classe):
				f = open(PATH_input+'/'+classe+'/'+f).readlines()
				for w in f:
					w = w.split()[0]
				
					#if w not in vocabulary_cache:
					if w not in vocabulary:
						vocabulary[w] = 0
					vocabulary[w] += 1
	
	vocabulary = zip(vocabulary.values(),vocabulary.keys())
	vocabulary.sort()
	vocabulary = vocabulary[::-1]
	
	for v in vocabulary:
		v_file.write(v[1]+'\n')
	v_file.close()
	
PATH_input = sys.argv[1]
file_name = sys.argv[2]
increaseVocabulary(PATH_input,file_name)







		
