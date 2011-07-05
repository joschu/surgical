"""
Based on expt_fancy_twist, but now we're using the controllers module

"""

from __future__ import division
from doo.doo import Thread
from mp.utils import colorSeq
import numpy as np
from numpy import pi
from numpy.random import randn
import mayavi.mlab as mlab
import sys
import controllers as C


def test_bend_first():
    thread = Thread()
    mlab.figure(1); mlab.clf()
    T = 16
    
    colors = colorSeq(25)
    
    for (t,cons) in enumerate(C.bend_first(thread,1,.1)):
        thread.setConstraints(cons)
        x,y,z = thread.getXYZ()
        mlab.plot3d(x,y,z,tube_radius=.1,color=colors.next())
        if t == 10: break

def test_bend_last():
    thread = Thread()
    mlab.figure(2); mlab.clf()
    T = 16
    
    colors = colorSeq(25)
    
    for (t,cons) in enumerate(C.bend_last(thread,1,.1)):
        thread.setConstraints(cons)
        x,y,z = thread.getXYZ()
        mlab.plot3d(x,y,z,tube_radius=.1,color=colors.next())
        if t == 10: break

def test_bend_ends():
    thread = Thread()
    mlab.figure(3); mlab.clf()
    T = 16
    
    colors = colorSeq(25)
    
    for (t,cons) in enumerate(C.bend_ends(thread,1,.1)):
        thread.setConstraints(cons)
        x,y,z = thread.getXYZ()
        mlab.plot3d(x,y,z,tube_radius=.1,color=colors.next())
        

def test_move_ends():
    thread = Thread()
    mlab.figure(1); mlab.clf()
    
    colors = colorSeq(25)
    
    cons_new = thread.getConstraints()
    cons_new[0:3] += 4
    cons_new[6:9] += 4
    
    for (t,cons) in enumerate(C.match_cons(thread,cons_new)):
        thread.setConstraints(cons)
        x,y,z = thread.getXYZ()
        mlab.plot3d(x,y,z,tube_radius=.1,color=colors.next())
    
def test_jumprope():
    thread = Thread()
    mlab.figure(1); mlab.clf()
    
    colors = colorSeq(100)
    
    cons_new = thread.getConstraints()
    
    for cons in C.bend_ends(thread,.25,.1):
        thread.setConstraints(cons)
    
    for (t,cons) in enumerate(C.jumprope(thread,pi,.1)):
        thread.setConstraints(cons)
        x,y,z = thread.getXYZ()
        mlab.plot3d(x,y,z,tube_radius=.1,color=colors.next())

def test_running_jumprope():        

    thread = Thread()
    mlab.figure(1); mlab.clf()
    
    
    colors = colorSeq(100)
    
    cons_new = thread.getConstraints()
    cons_new[0:3] += 25
    cons_new[6:9] += 25

    
    for cons in C.bend_ends(thread,.25,.1):
        thread.setConstraints(cons)

    rj = C.add_controllers(thread,C.translate_ends(thread,[0,0,30],20),
                           C.jumprope(thread,pi,.25))
    
    for (t,cons) in enumerate(rj):
        thread.setConstraints(cons)
        x,y,z = thread.getXYZ()
        mlab.plot3d(x,y,z,tube_radius=.1,color=colors.next())

def test_rotate_until_planes_aligned():  
    
    mlab.figure(1); mlab.clf()
    thread = Thread()
    thread_target = thread.clone()
    for cons in C.seq_controllers(C.translate_ends(thread_target,[0,30,0],20),
                                  C.bend_ends(thread_target,pi/4,.1),
                                  C.jumprope(thread_target,pi/3,.1)):
        thread_target.setConstraints(cons)
        x,y,z = thread_target.getXYZ()
        mlab.plot3d(x,y,z,tube_radius=.1,color=(1,1,1)) 

        
    colors = colorSeq(100)
    for cons  in C.match_cons(thread,thread_target.getConstraints()):
        thread.setConstraints(cons)
        x,y,z = thread.getXYZ()
        mlab.plot3d(x,y,z,tube_radius=.1,color=colors.next(),opacity=.5)    

    #for cons  in C.bend_ends(thread,pi/3,.1):
        #thread.setConstraints(cons)
        #x,y,z = thread.getXYZ()
        #mlab.plot3d(x,y,z,tube_radius=.1,color=colors.next())    
    
    #for cons  in C.cl_rotate(thread,thread_target):
        #thread.setConstraints(cons)
        #x,y,z = thread.getXYZ()
        #mlab.plot3d(x,y,z,tube_radius=.1,color=colors.next())
    
        
if __name__ == "__main__":
    #test_running_jumprope()
    #test_bend_ends()
    test_rotate_until_planes_aligned()