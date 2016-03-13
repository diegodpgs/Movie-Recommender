import os



def getTags(PATH):
	tags = {}

	for file_name in os.listdir(PATH):
		file_tag = open(PATH+file_name).read()
		file_tag = file_tag.split('\n')
		
	
		for tag in file_tag[:-1]:
			
			keyword = tag.split(';#;')[0]
			out     = int(tag.split(';#;')[1])
			total   = int(tag.split(';#;')[2])
		
			if keyword not in tags:
				tags[keyword] = [0,0]
		
			tags[keyword][0] += min(out,1)
			if out==total and out > 0:
				tags[keyword][0] += 1
				tags[keyword][1] += 1
			tags[keyword][1] += min(total,1)
			
			if '_' in keyword:
				for k in keyword.split('_'):
					if k not in 'in a on of the to by an from and '.split():
						if k not in tags:
							tags[k] = [0,0]
						
						tags[k][0] += min(out,1)
						tags[k][0] += min(total,1)
	
	return tags
	

no_PATH  = os.getcwd()+'/data/original_data/tags/all/no_1_7/'
yes_PATH = os.getcwd()+'/data/original_data/tags/all/yes_8_10/'

nodic  = getTags(no_PATH)
yesdic = getTags(yes_PATH) 

file_no = open('TAGS_NO.tags','w')
file_yes = open('TAGS_YES.tags','w')

no_tags = zip(nodic.values(),nodic.keys())
no_tags.sort()

yes_tags = zip(yesdic.values(),yesdic.keys())
yes_tags.sort()


for tag in no_tags[::-1]:
	file_no.write('%s;%d;%d;\n' % (tag[1],tag[0][0],tag[0][0]))
	

for tag in yes_tags[::-1]:
	file_yes.write('%s;%d;%d;\n' % (tag[1],tag[0][0],tag[0][0]))