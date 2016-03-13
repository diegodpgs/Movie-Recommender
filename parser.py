import nltk

#@ data['classe:yes_8_10,no_1_7']['genre:13 categories']['movie_name.srt']= [tokens]
def writeData(PATH_output,data):

	for classe, genres in data.iteritems():
	
		for genre,movies_file_names in genres.iteritems():
			for movie_file_name, tokens in movies_file_names.iteritems():
				movie_name = movie_file_name.split('.')[0]
				file_genre = open('%s/category/%s/%s/%s' % (PATH_output,classe,genre,movie_file_name),'w')
				file_all = open('%s/all/%s/%s' % (PATH_output,classe,movie_file_name),'w')
				
				for token in tokens:
					if movie_file_name != '.review':
						file_genre.write('%s %d\n' % (token[1],token[0]))
						file_all.write('%s %d\n' % (token[1],token[0]))

#@ data['classe:yes_8_10,no_1_7']['genre:13 categories']['movie_name.srt']= [tokens]
def applyThreshold(data,frequency_tokens,threshold=2):
	movies_computed = []

# 	ft = open('ftokens.txt','w')
# 	for key,value in frequency_tokens.iteritems():
# 		ft.write('%s %d\n' % (key,value))
		
	#print frequency_tokens.most_common(100)
	
	for classe, genres in data.iteritems():
		for genre,movies_file_names in genres.iteritems():
			for movie_file_name, tokens in movies_file_names.iteritems():
				
				print movie_file_name,'applying threshold'
				if movie_file_name in movies_computed:
					genres_keys = data[classe].keys()
					index = 0
					
					while movie_file_name not in data[classe][genres_keys[index]]:
						index += 1
					
					data[classe][genre][movie_file_name] = data[classe][genres_keys[index]][movie_file_name][:]
					
				else:	
					new_tokens_after_threshold = []
					freq = nltk.FreqDist(tokens)
					
					for token in set(tokens):
						
						if type(threshold) == type([]):
							if token in threshold:
								new_tokens_after_threshold.append((freq[token],token))
						
						elif frequency_tokens[token] > threshold:
							new_tokens_after_threshold.append((freq[token],token))
				
					new_tokens_after_threshold.sort()
					data[classe][genre][movie_file_name] = new_tokens_after_threshold[::-1]
				
					movies_computed.append(movie_file_name)
	
	return data

