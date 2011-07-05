from __future__ import division
from doo.doo import Thread
from mp.utils import upsample2D
import numpy as np
from numpy.random import randn
import mayavi.mlab as mlab
import sys
import twists

np.random.seed(1)
# seed with 0 and final config is the same
# seed with 1 and it's way different

scale = .25
T = 10

thread_start = Thread()
n_clones = 2
threads = [thread_start.clone() for _ in xrange(n_clones)]

cons_start = thread_start.getConstraints()
cons_end = cons_start + scale*np.r_[randn(3)*10,randn(3)*.5,randn(3)*10,randn(3)*.5]

tip1_start,tip2_start = cons_start[0:3],cons_start[6:9]
tip1_end,tip2_end = cons_end[0:3],cons_end[6:9]
tips = np.c_[tip1_start,tip2_start,tip1_end,tip2_end]


colors = [(1,0,0),(0,1,0),(0,0,1)]

mlab.figure(1); mlab.clf()

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
        if t==T-1: mlab.plot3d(x,y,z,color=color,tube_radius=.1)

    
#ang = -twists.opt_rot(threads[0].getXYZ(),threads[1].getXYZ())
thread = threads[0]
target_thread = threads[1]
for (t,cons) in enumerate(twists.jumprope2(thread,target_thread = target_thread)):
    thread.setConstraints(cons)
    x,y,z = thread.getXYZ()
    mlab.plot3d(x,y,z,color=tuple(np.clip([t/25,t/25,1],0,1)),tube_radius=.1)
                     
#for (t,cons) in enumerate(twists.jumprope2(thread,target_thread = target_thread)):
    #thread.setConstraints(cons)
    #x,y,z = thread.getXYZ()
    #mlab.plot3d(x,y,z,color=tuple(np.clip([t/25,0,0],0,1)),tube_radius=.1)
    
#mlab.plot3d(x,y,z,color=tuple(np.clip([t/25,0,0],0,1)),tube_radius=.1)
        
        