stopwords = open('NSTOP_WORDS.stop').readlines()
newstop = open('STOPWORDS.stop','w')

for s in stopwords:
	if len(s) > 3 and s[3].isdigit():
		newstop.write(s[0:3]+';'+s[3:])
		print 'ok',s
		
	elif len(s) > 2 and s[2].isdigit():
		newstop.write(s[0:2]+';'+s[2:])
		
	elif len(s) > 1 and s[1].isdigit():
		newstop.write(s[0:1]+';'+s[1:])
		
	else:
		newstop.write(s)


