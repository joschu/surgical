from doo.doo import Thread
from mp.utils import *
from numpy import *
from numpy.random import randn
import mayavi.mlab as mlab
import sys
from doo import USCALE
from mp.simplectrl2 import *
import mp.plots as plots

# seed with 0 and final config is the same
# seed with 1 and it's way different

########## MAKE TARGET STATE


T = 30
scale = 5

thread_start = Thread()


cons_start = thread_start.getConstraints()

cons_end = cons_start + scale*USCALE*randn(12)
cons_mid = cons_start + scale*USCALE*randn(12)
cons_t = upsample2D(array([cons_start,cons_mid,cons_end]),T)
diffs = cons_t[:,6:9] - cons_t[:,0:3]
diffs = truncNorm(diffs,18)
cons_t[:,6:9] = cons_t[:,0:3] + diffs


mlab.figure(1); mlab.clf()

x,y,z = thread_start.getXYZ()
mlab.plot3d(x,y,z,tube_radius=.4,color=(1,1,1))
#x,y,z = tips
#mlab.points3d(x,y,z,color=(1,1,1))

thread = thread_start.clone()


for (t,cons) in enumerate(cons_t):
    print t
    thread.setConstraints(cons)
    #x,y,z = thread.getXYZ()

xyz = x,y,z = thread.getXYZ()
mlab.plot3d(x,y,z,color=(1,0,0),tube_radius=.4)
thread_targ = thread


####### GOTO ARCH

# guess a good arch
center = (xyz.T[0] + xyz.T[-1])/2
mainax = 10*normr(xyz.T[-1] - center)
up = xyz.T[xyz.shape[1]//2] - center
up -= normr(mainax) * dot(normr(mainax),up)


x,y,z = c_[center-mainax,center+mainax]
mlab.plot3d(x,y,z,color=(.8,.8,.8),tube_radius=.4)
x,y,z = c_[center,center+up]
mlab.plot3d(x,y,z,color=(.8,.8,.8),tube_radius=.4)
                 
elev = pi/2.5
p1_arch = center - mainax
p2_arch = center + mainax        
v1_arch = normr(mainax + normr(up)*norm(mainax)*tan(elev))
v2_arch = normr(mainax - normr(up)*norm(mainax)*tan(elev))

p1_now,v1_now,p2_now,v2_now = getState(thread_start)    

p1s = upsample2D(array([p1_now,p1_arch]),T,1)
p2s = upsample2D(array([p2_now,p2_arch]),T,1)    
v1s = upsample2D(array([v1_now,v1_arch]),T,1)
v2s = upsample2D(array([v2_now,v2_arch]),T,1)


colors = colorSeq(100)
thread = thread_start.clone()

for (p1,p2,v1,v2) in zip(p1s,p2s,v1s,v2s):
    col = colors.next()

    setOrs(thread,p1,v1,p2,v2)
    x,y,z = thread.getXYZ()
    mlab.plot3d(x,y,z,tube_radius=.075,color=col)

    #x,y,z = c_[p1,p1+3*v1]        
    #mlab.plot3d(x,y,z,tube_radius=.3,color=col)
    #x,y,z = c_[p2,p2+3*v2]        
    #mlab.plot3d(x,y,z,tube_radius=.3,color=col)

mlab.plot3d(x,y,z,tube_radius=.4,color=col)

####### GOTO TARG


p1_now,v1_now,p2_now,v2_now = getState(thread)    
p1_targ,v1_targ,p2_targ,v2_targ = getState(thread_targ)    
p1s = upsample2D(array([p1_now,p1_targ]),T,1)
p2s = upsample2D(array([p2_now,p2_targ]),T,1)    
v1s = upsample2D(array([v1_now,v1_targ]),T,1)
v2s = upsample2D(array([v2_now,v2_targ]),T,1)


for (p1,p2,v1,v2) in zip(p1s,p2s,v1s,v2s):
    col = colors.next()

    setOrs(thread,p1,v1,p2,v2)
    x,y,z = thread.getXYZ()
    mlab.plot3d(x,y,z,tube_radius=.075,color=col)

    #x,y,z = c_[p1,p1+3*v1]        
    #mlab.plot3d(x,y,z,tube_radius=.3,color=col)
    #x,y,z = c_[p2,p2+3*v2]        
    #mlab.plot3d(x,y,z,tube_radius=.3,color=col)

mlab.plot3d(x,y,z,tube_radius=.4,color=col)



### PLOT FINAL
mlab.figure(2); mlab.clf()
x,y,z = thread_targ.getXYZ()
mlab.plot3d(x,y,z,tube_radius=.4,color=(1,0,0))
x,y,z = thread.getXYZ()
mlab.plot3d(x,y,z,tube_radius=.4,color=(0,0,1))


### ORIENTATION PLOTS
plots.plotOrs(thread_targ.getXYZ().T,thread.getXYZ().T)