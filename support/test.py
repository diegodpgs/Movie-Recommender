import time
import random

tokens = list('abcd')
stop = list('fghijklmnopqrstuvxzyw123456790')


newt = list('abcdfghijklmnoprstuvxzyw123456790'*1000000)
random.shuffle(newt)

texto = ' '.join(newt)

newtext = []


t = time.time()
for n in newt:
	if n in tokens:
		newtext.append(n)

print time.time()-t


t = time.time()
for l in stop:
	if l in texto:
		texto = texto.replace(l,' %s ' % l)

print time.time()-t
	






