"""based on test_path_dependence"""

from doo.doo import Thread
from doo import USCALE
from mp.utils import upsample2D,colorSeq
import numpy as np
from numpy.random import randn
import mayavi.mlab as mlab
import sys
import mp.controllers as C

mlab.figure(1); mlab.clf()

scalar =5
T = 30
n_waypoints = 3

np.random.seed(23)
#np.random.seed(24)
#np.random.seed(28)

thread = Thread()
thread_targ = thread.clone()

cons = thread.getConstraints()
waypoints = cons[None,:] + np.cumsum(np.r_[np.zeros((1,12)),scalar*USCALE*randn(n_waypoints,12)],0)

for cons in upsample2D(waypoints,n_waypoints*T):
    thread_targ.setConstraints(cons)
    x,y,z = thread_targ.getXYZ()
    mlab.plot3d(x,y,z,tube_radius=.05,color=(1,1,1))

mlab.clf()

x,y,z = thread_targ.getXYZ()
mlab.plot3d(x,y,z,tube_radius=.2,color=(1,1,1))


colors = colorSeq(100)
x,y,z = thread.getXYZ()
mlab.plot3d(x,y,z,tube_radius=.2,color=colors.next())


for cons  in C.match_cons(thread,thread_targ.getConstraints()):
    thread.setConstraints(cons)
    x,y,z = thread.getXYZ()
    mlab.plot3d(x,y,z,tube_radius=.05,color=colors.next())    

for cons  in C.cl_rotate(thread,thread_targ):
    thread.setConstraints(cons)
    x,y,z = thread.getXYZ()
    mlab.plot3d(x,y,z,tube_radius=.05,color=colors.next())    

#for cons  in C.match_cons(thread,thread_targ.getConstraints()):
    #thread.setConstraints(cons)
    #x,y,z = thread.getXYZ()
    #mlab.plot3d(x,y,z,tube_radius=.05,color=colors.next())       
    
mlab.plot3d(x,y,z,tube_radius=.2,color=colors.next())    