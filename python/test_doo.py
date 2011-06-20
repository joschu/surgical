from doo import Thread,GLThread
from comm import readMats,writeMats
import enthought.mayavi.mlab as mlab
from time import sleep,time
import numpy as np
#t = Thread()
#t.printVertices()
#t.dump()
mlab.clf()

glt = GLThread()
glt = GLThread()

t_start = time()
A,B=glt.makePerts()
print "makeperts time",time()-t_start
#fig = plt.figure(1)
#from mpl_toolkits.mplot3d import Axes3D
#ax = fig.add_subplot(111,projection='3d')

glt.minimizeEnergy()
xyz,start_rot,end_rot = glt.getData()

glt.printThreadData()
cons = glt.getConstraints()
glt.setConstraints(cons + np.random.randn(12)*.1)


mlab.plot3d(xyz[0],xyz[1],xyz[2],tube_radius=.5,color=(1,0,0))

glt.minimizeEnergy()
xyz1,start_rot1,end_rot1 = glt.getData()
mlab.plot3d(xyz1[0],xyz1[1],xyz1[2],tube_radius=.5,color=(0,1,0))

