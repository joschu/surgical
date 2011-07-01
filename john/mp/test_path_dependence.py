from doo.doo import Thread
from mp.utils import upsample2D
import numpy as np
from numpy.random import randn
import mayavi.mlab as mlab
import sys

try:
    seed = int(sys.argv[-1])
    np.random.seed(seed)
    print "using seed", seed
except Exception:
    print "not using seed"

# seed with 0 and final config is the same
# seed with 1 and it's way different

scale = .25
T = 10

thread_start = Thread()
n_clones = 3
threads = [thread_start.clone() for _ in xrange(n_clones)]

cons_start = thread_start.getConstraints()
cons_end = cons_start + scale*np.r_[randn(3)*10,randn(3)*.5,randn(3)*10,randn(3)*.5]

tip1_start,tip2_start = cons_start[0:3],cons_start[6:9]
tip1_end,tip2_end = cons_end[0:3],cons_end[6:9]
tips = np.c_[tip1_start,tip2_start,tip1_end,tip2_end]


colors = [(1,0,0),(0,1,0),(0,0,1)]

mlab.clf()

x,y,z = thread_start.getXYZ()
mlab.plot3d(x,y,z,tube_radius=.4,color=(1,1,1))
#x,y,z = tips
#mlab.points3d(x,y,z,color=(1,1,1))

for (i,thread,color) in zip(xrange(n_clones),threads,colors):
    print "thread",i
    cons_mid = cons_start + scale*np.r_[randn(3)*10,randn(3)*.5,randn(3)*10,randn(3)*.5]
    cons_t = upsample2D(np.array([cons_start,cons_mid,cons_end]),T)
    thread = threads[i]
    for (t,cons) in enumerate(cons_t):
        print t
        thread.setConstraints(cons)
        x,y,z = threads[i].getXYZ()
        if t==T-1: tube_radius = .4
        else: tube_radius = .1
        mlab.plot3d(x,y,z,color=color,tube_radius=tube_radius)

        
        