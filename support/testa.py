import os
import nltk
#from utilsrt import *


no_srt = os.getcwd()+'/data/parsed_data/Review/all/no_1_7'
yes_srt = os.getcwd()+'/data/parsed_data/Review/all/yes_8_10'

files_no = os.listdir(no_srt)
files_yes = os.listdir(yes_srt)
total_tokens = []

stats = open('statistics_review_600.txt','w')
total = 0
statistics = {}
for file_name in files_no:
	print file_name
	count = 0
	if 'DS_Store' not in file_name:
		data_raw = open(no_srt+'/'+file_name).readlines()
		#stats.write(file_name+';              ')
		words = []
		for review in data_raw[0:600]:
			srt = review.replace('\n','')
			srt = review.split()
			words.append((srt[0],int(srt[1])))
		
		print 'compute words'
		for index1 in xrange(len(words)):
			for index2 in xrange(index1+1,len(words)):
				
				if words[index1][1] > words[index2][1]:
					key = '%s_<>_%s' % (words[index1][0],words[index2][0])
					
					if key not in statistics:
						statistics[key]= {'no':0,'yes':0}
					
					statistics[key]['no'] += 1
					


for file_name in files_yes:
	print file_name
	count = 0
	if 'DS_Store' not in file_name:
		data_raw = open(yes_srt+'/'+file_name).readlines()
		#stats.write(file_name+';              ')
		words = []
		for review in data_raw[0:600]:
			srt = review.replace('\n','')
			srt = review.split()
			words.append((srt[0],int(srt[1])))
		
		print 'compute words'
		for index1 in xrange(len(words)):
			for index2 in xrange(index1+1,len(words)):
				
				if words[index1][1] > words[index2][1]:
					key = '%s_<>_%s' % (words[index1][0],words[index2][0])
					
					if key not in statistics:
						statistics[key]= {'no':0,'yes':0}
					
					statistics[key]['yes'] += 1.0

#3MB 500
high = []
total = len(statistics)
count = 0.0
for key, values in statistics.iteritems():
	count += 1
	if (values['no']+values['yes'])>30:
		ratio = values['no']/(values['yes']+values['no'])
		high.append((ratio,values['no'],values['yes'],key))
	
	if count % 10000 == 0:
		print '%1.2f%% processed' % ((count/total)*100)

high.sort()
high = high[::-1]
total = len(high)
count = 0.0
for h in high:
	count += 1
	stats.write('%s;%1.2f;%d;%d\n' % (h[-1],h[0],h[1],h[2]))
	
	if count % 500 == 0:
		print '%1.2f%% written' % ((count/total)*100)