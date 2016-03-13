#
# @corpus
#		a list of words
#
# return
#		a map of unigrams
#
def getUnigram(corpus):
	dic_unigram = {}

	for token in corpus:
		if token not in dic_unigram:
			dic_unigram[token] = 1

		dic_unigram[token] += 1
	
	return dic_unigram

#
# @corpus
#		a list of words
#
# return
#		a map of bigrams
#
def getBigram(corpus):

	dic_bigram = {}
	list_bigram = []
	
	col_2 = corpus[:]
	col_2.append('#')
	col_1 = corpus[:]
	col_1.insert(0,'#')
	count = 0

	for index in xrange(len(col_1)):
		w1 = col_1[index]
		w2 = col_2[index]

		if w1 not in dic_bigram:
			dic_bigram[w1] = {}

		if w2 not in dic_bigram[w1]:
			dic_bigram[w1][w2] = 0

		dic_bigram[w1][w2] += 1
		list_bigram.append('%s_%s' % (w1,w2))
		

	return dic_bigram,list_bigram

#
# @corpus
#		a list of words
#
# return
#		a map of trigrams
#
def getTrigram(corpus):

	dic_trigram = {}
	
	
	col_1 = corpus[:]
	col_1.insert(0,'#')
	col_1.insert(0,'#')

	col_2 = corpus[:]
	col_2.insert(0,'#')
	col_2.append('#')

	col_3 = corpus[:]
	col_3.append('#')
	col_3.append('#')

	count = 0

	for index in xrange(len(col_1)):
		w1 = col_1[index]
		w2 = col_2[index]
		w3 = col_3[index]

		if w1 not in dic_trigram:
			dic_trigram[w1] = {}

		if w2 not in dic_trigram[w1]:
			dic_trigram[w1][w2] = {}

		if w3 not in dic_trigram[w1][w2]:
			dic_trigram[w1][w2][w3] = 0			

		dic_trigram[w1][w2][w3] += 1
		

	return dic_trigram


#
# @corpus
#		a list of words
#
# return
#		a map of fourgram
#
def getFourgram(corpus):
	"""
    	#	#	#	A
    	#	#	A   B
    	#   A   B   C
    	A   B   C   D
    	B	C	D	E
    	C   D   E   #
    	D   E   #   #
    	E   #   #   #

	"""
	dic_fourgram = {}
	cols = []

	for i in xrange(4):
		cols.append(corpus[:])
		for j in xrange(i,3):
			cols[-1].insert(0,'#')

		for j in xrange(4-i,4):
			cols[-1].append('#')

	
	count = 0
	size_cols = len(cols[0])

	for index in xrange(size_cols):
		ws = []

		for i in xrange(4):
			ws.append(cols[i][index])
		
		if ws[0] not in dic_fourgram:
			dic_fourgram[ws[0]] = {}

		if ws[1] not in dic_fourgram[ws[0]]:
			dic_fourgram[ws[0]][ws[1]] = {}

		if ws[2] not in dic_fourgram[ws[0]][ws[1]]:
			dic_fourgram[ws[0]][ws[1]][ws[2]] = {}

		if ws[3] not in dic_fourgram[ws[0]][ws[1]][ws[2]]:
			dic_fourgram[ws[0]][ws[1]][ws[2]][ws[3]] = 0

		dic_fourgram[ws[0]][ws[1]][ws[2]][ws[3]] += 1
		

	return dic_fourgram

#
# @ngram
#		type of ngram to sort
#
# return
#		a list of tokens sorted
#		[(count,tokens)]
#
def sortNgram(ngram):
	ngram_sorted = []

	#is it unigram?
	if detectNgram(ngram) == 1:
		ngram_sorted = zip(ngram.values(),ngram.keys())

	#is it bigram?
	elif detectNgram(ngram) == 2:

		 for unigram,bigram in ngram.iteritems():
		 	temp = [(count, "%s_%s" % (unigram,token)) for token,count in bigram.iteritems()]
		 	ngram_sorted.extend(temp)

	#is it trigram?
	elif detectNgram(ngram) == 3:
		for unigram_key,bigram in ngram.iteritems():
			for bigram_key,trigram in bigram.iteritems():

				temp = [(count, "%s_%s_%s" % (unigram_key,bigram_key,trigram_key)) for trigram_key,count in trigram.iteritems()]
		 		ngram_sorted.extend(temp)

	#then it is fourgram
	else:
		for unigram_key,bigram in ngram.iteritems():
			for bigram_key,trigram in bigram.iteritems():
				for trigram_key,fourgram in trigram.iteritems():
					temp = [(count, "%s_%s_%s_%s" % (unigram_key,bigram_key,trigram_key,fourgram_key)) for fourgram_key,count in fourgram.iteritems()]
		 			ngram_sorted.extend(temp) 

	ngram_sorted.sort()
	return ngram_sorted


def detectNgram(ngram):
	if type(ngram.values()[0]) == int:
		return 1

	elif type(ngram.values()[0].values()[0]) == int:
		return 2

	elif type(ngram.values()[0].values()[0].values()[0]) == int:	
		return 3

	return 4

def test():
	corpus = "a b c d a b c a d d d a b c d a d b".split()
	print sortNgram(getUnigram(corpus))
	print sortNgram(getBigram(corpus))
	print sortNgram(getTrigram(corpus))
	print sortNgram(getFourgram(corpus))










