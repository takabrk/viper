import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.path import Path
import matplotlib.patches as patches
from pylab import *
from numbers_list import *
ra = []
rb = []
rc = []
rx = []
listx = []
for i in range(30):
	listx.append(list3[i])
for i in listx:
	ra.append(i[1]/100)
	rb.append(i[1]%100/10)
	rc.append(i[1]%100%10)
	rx.append(i[0])
"""
mpl.rcParams["patch.facecolor"] = "none"
fig = plt.figure()
ax1 = fig.add_subplot(111)
verts = [(0., 0.), (2., 4.), (4., 0.)]
codes = [Path.MOVETO,Path.CURVE3,Path.CURVE3]
path = Path(verts,codes)
patch = patches.PathPatch(path)
ax1.add_patch(patch)
"""
#f = np.poly1d([1,-4,3])
#xs = np.arange(-2,4,0.1)
#ys = [f(x) for x in xs]
plt.plot(rx,ra)
plt.plot(rx,rb)
plt.plot(rx,rc)
#plt.show()
savefig("graph.png")
#f=open("test2.txt","w")
#f.write(str(np.histogram(ra)))
#f.close()
