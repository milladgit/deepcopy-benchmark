

import os,sys

template = "python run.py %d %d %d"

d = dict()
d[10] = 50
d[100] = 50
d[1000] = 30
d[10000] = 30
d[100000] = 20
d[1000000] = 10
d[10000000] = 10
d[100000000] = 10


count = 0

for i in range(2,11):
#for i in [10]:
	ten = 10
	for j in range(8):
		cmd = template % (i, ten, d[ten])
		print cmd
		os.system(cmd)
		count += 1
		ten *= 10

print count

