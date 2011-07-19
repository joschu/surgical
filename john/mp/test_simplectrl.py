"""
Based on expt_fancy_twist, but now we're using the controllers module

"""

from __future__ import division
from doo.doo import Thread
from mp.utils import colorSeq
import numpy as np
from numpy import pi,r_
from numpy.random import randn
import mayavi.mlab as mlab
from simplectrl import makeArch
from time import sleep
from itertools import izip

if __name__ == "__main__":
    
    thread = Thread()
    
    mlab.figure(1); mlab.clf()
    T = 20
    
    colors = colorSeq(100)
    
    for (t,cons) in izip(xrange(T),makeArch(thread,r_[0,0,0],r_[0,10,0],r_[0,0,5],0)):
        thread.setConstraints(cons)
        x,y,z = thread.getXYZ()
        mlab.plot3d(x,y,z,tube_radius=.1,color=colors.next())
        sleep(.1)
