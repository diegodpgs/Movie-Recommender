import os
#  X  >  y      no yes
#just_<>_do;0.77;33;10

mx = .7
mn = .3
	
def getStatistics(file_name='statistics_srt_400.txt'):

	keywords = open(file_name).read()
	keywords = keywords.split('\n')

	tokens_dic = {}
	
	for keyword in keywords[:-1]:
		token = keyword.split(';')[0]
		percent = float(keyword.split(';')[1])
	
		if percent > mx or percent < mn:
			tokens_dic[token] =  percent

	print 'Total of %d tokens' % len(tokens_dic)
	return tokens_dic

def processFile(data,tokens_dic):
	movie_tokens = {}
	for m in data[:-1]:
		movie_tokens[m.split()[0]] = int(m.split()[1])

	no = 0
	yes = 0
	none = 0

	for token,freq in tokens_dic.iteritems():
		left  = token.split('_<>_')[0]
		right = token.split('_<>_')[1]

		if left in movie_tokens and right in movie_tokens:
		
			if movie_tokens[left] > movie_tokens[right]:
				if freq > mx:
					no += 1
				elif freq < mn:
					yes += 1
			elif freq > mx:
				yes += 1
			elif freq < mn:
				no += 1
		else:
			none += 1
	
	return (no,yes,none)


def run(PATH):
	summary = {'no':0,'yes':0,'none':0}
	ok = 0
	fail = 0
	tokens_dic = getStatistics('statistics_srt_500.txt')
	all_results = []
	
	for file_name in os.listdir(PATH):
		movie = open(PATH+'/'+file_name).read()
		movie = movie.split('\n')
		no,yes,none = processFile(movie[0:500],tokens_dic)
		
		
		if yes+no > 0:
			summary['no'] += no
			summary['yes'] += yes
			summary['none'] += none
			r = yes/float(no+yes)
			
			if yes > no:
				ok += 1
				all_results.append((r,file_name,'----------OK'))
			else:
				fail += 1
				all_results.append((r,file_name,''))

			
			

	
	all_results.sort()
	return (summary,ok,fail,all_results[::-1])

summary,ok,fail,all_results = run(os.getcwd()+'/data/parsed_data_new/SRT/all/yes_8_10')
print 'No: %d\nYes: %d\n None: %d\n Accuracy: %1.2f' % \
	(summary['no'],summary['yes'],summary['none'],
	summary['yes']/float(summary['no']+summary['yes']))

print 'OK: %d Fail: %d Accuracy: %1.2f' % (ok,fail,ok/float(ok+fail))
for r in all_results:
	print '%s %1.3f %s' % (r[1].ljust(38),r[0],r[2].ljust(20))