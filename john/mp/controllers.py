from __future__ import division
from nibabel.eulerangles import euler2mat,angle_axis2euler,mat2euler
from nibabel.quaternions import angle_axis2mat
import numpy as np
from numpy import arccos,dot,cross,linspace,empty,pi,ceil,arange,asarray
from numpy.linalg import norm
from itertools import izip_longest,chain
from mp.utils import trunc
from doo import USCALE

def apply_rot_eul(eul,ang,ax):
    "compose a rotation of ang around ax with rotation given by euler angles eul"
    return mat2euler(dot(angle_axis2mat(ang,ax),euler2mat(*eul)))

def apply_rot_vec(x,ang,ax,origin):
    "rotate a vector x by ang around axis defined by ray origin+ax"
    return dot(angle_axis2mat(ang,ax),x-origin[:,None])+origin[:,None]

def ang_between(vec1,vec2):
    "angle between vectors, in range [0,pi]"
    return arccos(dot(vec1,vec2)/norm(vec1)/norm(vec2))

def jumprope(thread,theta,dtheta):
    "rotate ends around axis joining them"
    for _ in xrange(int(ceil(abs(theta/dtheta)))):
        cons = thread.getConstraints()
        ax_rot = cons[6:9]-cons[0:3]
        cons[3:6] = apply_rot_eul(cons[3:6],dtheta,ax_rot)
        cons[9:12] = apply_rot_eul(cons[9:12],dtheta,ax_rot)
        yield cons
        
def cl_rotate(thread,xyz_targ):


    #xyz_targ = thread_target.getXYZ()
        
    thread1 = thread.clone()
    dists1 = []
    for cons in jumprope(thread1,pi/4,pi/16):
        thread1.setConstraints(cons)
        dists1.append(norm(xyz_targ - thread1.getXYZ()))
    
    thread2 = thread.clone()
    dists2 = []
    for cons in jumprope(thread2,-pi/4,pi/16):
        thread2.setConstraints(cons)
        dists2.append(norm(xyz_targ - thread2.getXYZ()))
    
    if min(dists1) < min(dists2): dtheta = .1
    else: dtheta = -.1
    

    for cons in jumprope(thread,2*pi,dtheta):
        dist1 = norm(xyz_targ - thread.getXYZ())
        clone = thread.clone()
        clone.setConstraints(cons)
        dist2 = norm(xyz_targ - clone.getXYZ())
        if dist2 > dist1: break

        yield cons
        
    #for cons in match_cons(thread,thread_target.getConstraints()):
        #yield cons
    
    
def twist_first(thread,theta,dtheta):        
    while True:
        xyz = thread.getXYZ()
        ax_rot = xyz[:,1] - xyz[:,0]
        cons = thread.getConstraints()
        for _ in xrange(int(ceil(abs(theta/dtheta)))):
            cons[3:6] = apply_rot_eul(cons[3:6],dtheta,ax_rot)
            yield cons
        

#def estimate_twist(thread):
    #xyz = thread.getXYZ()
    #o
            
def bend_first(thread,theta,dtheta):
    """if angle between ends and line joining them is less than theta
    bend the ends outwards"""
        
    while True:
        xyz = thread.getXYZ()
        ax_main = xyz[:,-1] - xyz[:,0]
        ax_tan = xyz[:,1] - xyz[:,0]
        ax_rot = cross(ax_main,xyz[:,2]-xyz[:,0]) 
        # .9,.1 is to make sure it's not zero
        cons = thread.getConstraints()
        if ang_between(ax_main,ax_tan) < theta:
            print "first",ang_between(ax_main,ax_tan),ax_rot            
            cons[3:6] = apply_rot_eul(cons[3:6],dtheta,ax_rot)
            yield cons
        else:
            break
        
def bend_last(thread,theta,dtheta):
    """if angle between ends and line joining them is less than theta
    bend the ends outwards"""
        
    while True:
        xyz = thread.getXYZ()
        ax_main = xyz[:,0] - xyz[:,-1]
        ax_tan = xyz[:,-2] - xyz[:,-1]
        ax_rot = cross(ax_main,xyz[:,-3]-xyz[:,-1]) # make sure it's not zero
        cons = thread.getConstraints()
        if ang_between(ax_main,ax_tan) < theta:
            print "last",ang_between(ax_main,ax_tan),ax_rot
            cons[9:12] = apply_rot_eul(cons[9:12],dtheta,ax_rot)
            yield cons
        else:
            break
            
def bend_ends(thread,theta=.5,dtheta=.1):
    return add_controllers(thread,bend_first(thread,theta,dtheta),bend_last(thread,theta,dtheta))

def match_cons(thread,cons_target,scaler=.5):
    while True:
        cons_cur = thread.getConstraints()
        dcons = cons_target-cons_cur
        if norm(dcons) < .1: break
        yield cons_cur + trunc(dcons,USCALE*scaler)

def translate_ends(thread,v,n):
    v = asarray(v)
    for _ in xrange(n):
        cons_cur = thread.getConstraints()
        cons_cur[0:3] += v/n
        cons_cur[6:9] += v/n
        yield cons_cur
        
        
def add_controllers(thread,cont1,cont2):
    """return another controller that applies them both at the same time
    and adds the results (i.e., adds the change in constraints)
    when one finishes, it just uses the other one"""
    for cons1,cons2 in izip_longest(cont1,cont2):            
        cons_cur = thread.getConstraints()
        if cons1 is None: cons1 = cons_cur
        if cons2 is None: cons2 = cons_cur
        yield cons1 + cons2 - cons_cur

        
        
def seq_controllers(*conts):
    return chain(*conts)

