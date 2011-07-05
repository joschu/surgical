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

T = 15
BEND = pi/6
TWIST = 2*pi



thread = Thread()
x,y,z = thread.getXYZ()
#mlab.plot3d(x,y,z,tube_radius=.4,color=(1,1,1))

mlab.figure(1); mlab.clf()
for t in xrange(T):
    twists.twist_around_axis(thread,BEND/T,-BEND/T,[0,1,0])
    x,y,z = thread.getXYZ()
    mlab.plot3d(x,y,z,tube_radius=.1,color=(1-t/T,0,t/T))

mlab.figure(2); mlab.clf()
for t in xrange(T):
    #twists.twist_ctrl(thread,2*np.pi/T,0)
    twists.twist_around_axis(thread,TWIST/T,TWIST/T,[1,0,0])
    x,y,z = thread.getXYZ()
    mlab.plot3d(x,y,z,tube_radius=.1,color=(1-t/T,0,t/T))


#x,y,z = tips
#mlab.points3d(x,y,z,color=(1,1,1))

        