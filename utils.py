import nltk
import time
from sequences import *

def tokenize(data_raw,file_stop_words):
	punct = list('.,:;!"<>/#)(&[]?*$')


	data_raw = data_raw.lower()

	for p in punct:
		data_raw = data_raw.replace(p,' ')
	data_raw = data_raw.replace("'",' ')
	data_raw = data_raw.replace('-',' ')
	
	data_raw = data_raw.split()
	bigrams = getBigram(data_raw)[1]
	new_data = data_raw[:]
	t = time.time()
	
	
	try:
		tokens_tag = nltk.pos_tag(data_raw)
	
		for tt in tokens_tag:
			if tt[1] == 'NN':
				new_data.append(tt[0])
	except:
		print 'exception'
		new_data = data_raw[:]
	print 'nltk.pos_tag() runtime: ',time.time()-t
	
	
	new_data.extend(bigrams)
	new_data.sort()
	return new_data

def removeStopWords(text,file_stop_words):

		stopwords = open(file_stop_words).read()
		stopwords = stopwords.split('\n')
		stopwords.sort()
		text.sort()
		cache = []
		new_text = []

		if len(text) > 1:
			index = 0
			previous = ''
			for index in xrange(len(text)):

				t = text[index]
				indexstop = lastIndex(index,t,stopwords)
				
				if indexstop == -1:
					new_text.append(t)
				else:
					stopwords = stopwords[indexstop:]
				
		
		return new_text


def lastIndex(index,token,stopwords):

	try:
		ti = time.time()
		new_index = stopwords.index(token)
		return new_index
	except:
		return -1
		

def convertToMiliseconds(time_data):
	separator = ','
	
	if '.' in time_data:
		separator = '.'
	hour    = int(time_data.split(':')[0])*3600000
	minutes = int(time_data.split(':')[1])*60000
	seconds = int(time_data.split(':')[2].split(separator)[0])*1000
	mili = int(time_data.split(':')[2].split(separator)[1])
	
	return hour+minutes+seconds+mili
	
def counttime(line):
	time1 = convertToMiliseconds(line.split('-->')[0])
	time2 = convertToMiliseconds(line.split('-->')[1])
	
	return time1,time2

def summaryGap(gaps):
	maxgap = 0
	mingap = 2147483646
	maxspeech = 0
	minspeech = 2147483646
	totalspeech = 0
	totalgap = 0
	
	previoustime2 = gaps[0][1]
	
	for time1,time2 in gaps[1:]:
		dif = time2-time1
		difprevious = time1-previoustime2
		previoustime2 = time2
		totalspeech += dif
		totalgap += difprevious
		
		if difprevious > maxgap:
			maxgap = difprevious
		
		elif difprevious < mingap:
			mingap = difprevious
		
		
		if dif > maxspeech:
			maxspeech = dif
		
		elif dif < minspeech:
			minspeech = dif
	
	averagegap = totalgap/float(len(gaps))
	averagespeech = totalspeech/float(len(gaps))
	
	return {'gap':(mingap,maxgap),'speech':(minspeech,maxspeech),'totalspeech':totalspeech,'totalgap':totalgap,'avgap':averagegap,'avgspeech':averagespeech}

def printsummary(summary):

	print 'GAP:%d,%d' % (summary['gap'][0],summary['gap'][1]),
	print 'SPEECH:%d,%d' % (summary['speech'][0],summary['speech'][1])	
	print 'TotalGap:%d' % (summary['totalgap'])
	print 'TotalSpeech:%d' % (summary['totalspeech']) 
	print 'AVG_gap:%1.2f' % (summary['avgap'])
	print 'AVG_speech:%1.2f' % (summary['avgspeech'])
	
