
import os, sys

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from pylab import meshgrid



def recursiveDS(q,n):
	if q == 0:
		return 12 + 8*n

	return 24+8*n+q*recursiveDS(q-1, n)



q = range(0,5)
n = range(100,10000000,100)

print len(q)
print len(n)

X,Y = meshgrid(n, q)
Z = np.sin(2*np.abs(X-0.3)+2*np.sin(5*Y))   
for i in range(len(q)):
	for j in range(len(n)):
		Z[i][j] = recursiveDS(q[i], n[j])

# for i in range(len(q)):
# 	for j in range(len(n)):
# 		print q[i], n[j], Z[i][j] 


fig = plt.figure()
# ax = fig.gca(projection='3d')
# surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
#                        linewidth=0, antialiased=False)

ax = fig.add_subplot(1, 1, 1, projection='3d')
p = ax.plot_wireframe(X, Y, Z)


# ax.plot_surface(X, Y, Z)
plt.show()
