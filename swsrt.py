import os
import nltk
from utilsrt import *


no_srt = os.getcwd()+'/data/parsed_data/SRT/all/no_1_7'
yes_srt = os.getcwd()+'/data/parsed_data/SRT/all/yes_8_10'

files_no = os.listdir(no_srt)
files_yes = os.listdir(yes_srt)
total_tokens = []

file_tokens = open('SRT_tokens.txt','w')
total = 0

for file_name in files_no:
	total += 1
	if 'DS_Store' not in file_name:
		data_raw = open(no_srt+'/'+file_name).read()
		data_raw = data_raw.replace('\n',' ')
		tokens = set(tokenize(data_raw,''))
		total_tokens.extend(tokens)
		print file_name,'computed',total,'of 207'

for file_name in files_yes:
	total += 1	
	if 'DS_Store' not in file_name:
		data_raw = open(yes_srt+'/'+file_name).read()
		data_raw = data_raw.replace('\n',' ')
		tokens = set(tokenize(data_raw,''))
		total_tokens.extend(tokens)
		print file_name,'computed',total,'of 207'

	
	

f = nltk.FreqDist(total_tokens)
f = zip(f.values(),f.keys())
f.sort()
f = f[::-1]

for token in f:
	file_tokens.write('%s;%d\n' % (token[1],token[0]))

	

	