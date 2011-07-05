from __future__ import division
from doo.doo import Thread
from mp.utils import upsample2D
import numpy as np
from numpy import pi
from numpy.random import randn
import mayavi.mlab as mlab
import sys
from nibabel.eulerangles import angle_axis2euler
import twists

BEND = pi/6
TWIST = 2*pi



thread = Thread()
xyz0 = thread.getXYZ()
#mlab.plot3d(x,y,z,tube_radius=.4,color=(1,1,1))
mlab.figure(1); mlab.clf()
T = 16

for (t,cons) in enumerate(twists.jumprope2(thread,pi)):
    #twists.twist_ctrl(thread,2*np.pi/T,0)
    thread.setConstraints(cons)
    x,y,z = thread.getXYZ()
    mlab.plot3d(x,y,z,tube_radius=.1,color=(1-t/T,0,t/T))

xyz = np.array([x,y,z])

print twists.opt_rot(xyz,xyz0)
#x,y,z = tips
#mlab.points3d(x,y,z,color=(1,1,1))

for (t,cons) in enumerate(twists.jumprope2(thread,pi)):
    #twists.twist_ctrl(thread,2*np.pi/T,0)
    thread.setConstraints(cons)
    x,y,z = thread.getXYZ()
    mlab.plot3d(x,y,z,tube_radius=.1,color=(0,t/T,1-t/T))

