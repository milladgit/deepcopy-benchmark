

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

iter_count = 20


k = 4
while k <= 128:
	ten = 10000
	while ten <= 10000000:
		n = ten
		x = 24 + 8*n
		y = 12 + 8*n

		B = x + k*(x+k*(x+k*(y)))

		GB = B/1024.0/1024.0/1024.0

		if GB <= 15.00:
			cmd = template % (k, n, iter_count)
			print cmd
			os.system(cmd)
			count += 1

		ten *= 2

	k *= 2


print count

