from settings import *
from doo import Thread
from sqp import frPath,calcStates,evalDiff
from numpy.random import randn
from utils import upsample2D

T = 20

thread = Thread()
scale=.25

cons_start = thread.getConstraints()
cons_1 = cons_start + scale*np.r_[randn(3)*10,randn(3)*.5,randn(3)*10,randn(3)*.5]
cons_2 = cons_start + scale*np.r_[randn(3)*10,randn(3)*.5,randn(3)*10,randn(3)*.5]
cons_end = cons_start + scale*np.r_[randn(3)*10,randn(3)*.5,randn(3)*10,randn(3)*.5]

print "moving thread to config 1 so it's hopefully stable"
cons_t = upsample2D(np.array([cons_start,cons_1]),T)
for cons in cons_t:
    thread.setConstraints(cons)

    
print "moving it along path 1->2->goal"    
cons_t = upsample2D(np.array([cons_1,cons_2,cons_end]),T)
import mayavi.mlab as mlab


xyzs_fwd = []
for cons in cons_t[1:]:
    thread.setConstraints(cons)
    x,y,z = thread.getXYZ()
    mlab.plot3d(x,y,z,tube_radius=.1,color=(1,0,0))
    
    
xyzs_back = []
for cons in cons_t[-1::-1]:
    thread.setConstraints(cons)
    x,y,z = thread.getXYZ()
    mlab.plot3d(x,y,z,tube_radius=.1,color=(0,0,1))

mlab.show()
    


