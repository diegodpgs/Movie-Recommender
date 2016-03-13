import random
import os

def selectData(size,file_data):
	samples_selected = []
	
	
	while len(samples_selected) < size and file_data.count('READ') != len(file_data):
		index_random = random.randint(0,len(file_data)-1)
		
		if file_data[index_random] != 'READ':
			samples_selected.append(file_data[index_random])
			file_data[index_random] = 'READ'
	
	return samples_selected,file_data

def build(data_no,data_yes,size_no,size_yes,step='train'):
	
	
	
	step_file = open('%s.txt' % step,'w')
	
	step_file.write('name;GAP_min;GAP_max;AVG_gap;AVG_speech;ratio;target\n')
	no_list,data_no = selectData(size_no,data_no)
	yes_list,data_yes =  selectData(size_yes,data_yes)
	
	for y in yes_list:
		y = y.replace('\n','')
		step_file.write(y)
		step_file.write(';1.0\n')
	
	for n in no_list:
		n = n.replace('\n','')
		step_file.write(n)
		step_file.write(';-1.0\n')
	
	return data_yes,data_no

data_no  = open('numericfeatures_no_1_7.txt').readlines()[1:]
data_yes = open('numericfeatures_yes_8_10.txt').readlines()[1:]
data_yes,data_no = build(data_no,data_yes,25,35,'train')

size = min(len(data_yes)-data_yes.count('READ'),len(data_no)-data_no.count('READ'))
build(data_no,data_yes,size,size,'test')
	
	 


	