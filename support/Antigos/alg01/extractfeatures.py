import os

def extractfeatures(file_data):
	features = file_data[-1].split('|')
	features = [(f.split(':')[0],f.split(':')[1]) for f in features]
	
	gap    		= (features[0][1].split(',')[0],features[0][1].split(',')[1])
	speech 		= (features[1][1].split(',')[0],features[1][1].split(',')[1])
	totalgap	= features[2][1]
	totalspeech = features[3][1]
	avg_gap 	= features[4][1]
	avg_speech	= features[5][1]
	
	return gap,speech,totalgap,totalspeech,avg_gap,avg_speech

def writeFeaturesFile(PATH):
	foldername = PATH.split('/')[-1]
	
	file_features = open('/Users/happyhour/Documents/Recomender/alg01/numericfeatures_%s.txt' % foldername,'w')
	file_features.write('name;GAP_min;GAP_max;AVG_gap;AVG_speech;ratio\n')
	
	for file_name in os.listdir(PATH):
		features = extractfeatures(open(PATH+'/'+file_name).readlines())
		
		file_features.write('%s;' % file_name.split('.srt')[0][1:])
		
		file_features.write('%d;' % max(int(features[1][0]),0))
		file_features.write('%d;' % min(int(features[1][1]),2147483647))
		
		for f in features[4:]:
			file_features.write(f+';')
		file_features.write('%1.3f\n' % (float(features[-1])/float(features[-2])))
	file_features.close()

writeFeaturesFile('/Users/happyhour/Documents/Recomender/parsed_data/no_1_7')
writeFeaturesFile('/Users/happyhour/Documents/Recomender/parsed_data/yes_8_10')

