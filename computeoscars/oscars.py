#coding: UTF-8
import urllib2

MONTH_TODAY = 10
DAY_TODAY = 8
YEAR_TODAY = 2015
#oscarfile = open('oscarsnames.txt').read()
OSCARS_NAMES = ['']

def getDate(data):
	birthDate = '00-00-00'
	deathDate = 'ALIVE'
	age = 0
		
	for line in data:
		line = line.replace('\n','')
		if '<time datetime=' in line:
			if 'birthDate' in line:
				birthDate = line.split('<time datetime="')[1].split('" itemprop')[0]
			elif 'deathDate' in line:
				deathDate = line.split('<time datetime="')[1].split('" itemprop')[0]
	
	birthDate = birthDate.split('-')
	try:
		byear =  int(birthDate[0])
		bmonth = int(birthDate[1])
		bday =   int(birthDate[2])
	except:
		byear,bmonth,bday = 0,0,0
	
	if deathDate != 'ALIVE':
		deathDate = deathDate.split('-')
		dyear =  int(deathDate[0])
		dmonth = int(deathDate[1])
		dday =   int(deathDate[2])
		
		if dmonth > bmonth or (dmonth == bmonth and dday >= bday):
			age = dyear - byear
		
		else:
			age = dyear - byear - 1
	
	else:
		if MONTH_TODAY > bmonth or (MONTH_TODAY == bmonth and DAY_TODAY >= bday):
			age = YEAR_TODAY - byear
		else:
			age = YEAR_TODAY - byear - 1
		

		
	if len(birthDate[1]) != 2:
		birthDate[1] = '0' + birthDate[1] 
	if len(birthDate[2]) != 2:
		birthDate[2] = '0' + birthDate[2]
		
	return int(birthDate[0]+birthDate[1]+birthDate[2]),age

def getNameOscars(file_name):
	nominated = 0
	won = 0
	name = ''
	data = urllib2.urlopen(file_name+'awards?ref_=nm_awd').readlines()
	

	for index_line in xrange(len(data)):

		line = data[index_line].replace('\n','')
		if "<meta property='og:title' content=" in line:
			name = line.split("<meta property='og:title' content=")[1]
			name = name.split('" />')[0][1:]
			
		
		
		if '"award_category">Oscar<' in line:
			#print name
			number = data[index_line-2].split('rowspan="')[1]
			number = int(number.split('"')[0])
		
			if 'Nominated' in data[index_line-1]:
				nominated += number
			elif 'Won' in data[index_line-1]:
				won += number
				
	
	
	#birth,age = getDate(urllib2.urlopen(file_name).readlines())
	
	return {'name':name,'won':won,'nominated':nominated}

def parserFile(file_url):

	winnerfound = False
	winners = []
	for line in urllib2.urlopen(file_url):
		line = line.replace('\n','')
		if '<h3>WINNER</h3>' in line:
			winnerfound = True
	
		if winnerfound:

			if '/name/' in line:
				win = line.split('/name/')[1]
				win = '/name/'+win.split('"')[0]
				winners.append('http://www.imdb.com'+win)
		
	
		if '<h3>NOMINEES</h3>' in line:
			winnerfound = False
	
		if '<h1>Honorary Award</h1>' in line:
			break
	
	return winners


def equals(win1,win2):
	return win1[0] == win2[0] and win1[1]==win2[1] and win1[2]==win2[2]
	
def partition(vector,start,end):
	pivo = vector[end]
	
	i = start - 1
	
	for j in range(start,end):
		
		if equals(vector[j][0],pivo[0]) and vector[j][0][-1] <= pivo[0][-1]:
			i = i + 1
			aux = vector[j]
			vector[j] = vector[i]
			vector[i] = aux
			
	aux = vector[end]
	vector[end] = vector[i+1]
	vector[i+1] = aux
      
	return i + 1

def QuickSort(vector, start, end):

		if start < end:
			indiceDoPivo = partition(vector, start,end)
			QuickSort(vector, start, indiceDoPivo -1) 
			QuickSort(vector, indiceDoPivo + 1, end)	
	
def run():
	win_file = open('winners.txt','w')
	ranking = {}
	url = 'http://www.imdb.com/event/ev0000003/'
	for year in xrange(2005,2016):
		winners = parserFile(url+str(year))

		for w in winners:
			winner = getNameOscars(w)
			
			if winner == None:
				continue

			if winner['name'] not in ranking:
				ranking[winner['name']] = (winner['won'],winner['nominated'],winner['age'],winner['birth'])
		
		print year,'......................processed'
	
	rankingsorted = zip(ranking.values(),ranking.keys())
	rankingsorted.sort()
	rankingsorted = rankingsorted[::-1]
	
	#QuickSort(rankingsorted,0,len(rankingsorted)-1)
	
	for winner in rankingsorted:
		win_file.write(winner[1]+';')
		win_file.write(str(winner[0][0])+';')
		win_file.write(str(winner[0][1])+';')
		win_file.write(str(winner[0][2])+';')
		win_file.write(str(winner[0][3])+'\n')

	



# if "__main__":
# 	run()
	
	
