from __future__ import division
from settings import *
from doo import Thread
from time import sleep,time
from utils import cprint
from logging import Logger
from numpy.linalg import norm

def calcFeats(xyzFlat):
    return xyzFlat
    xyz = xyzFlat.reshape(3,-1)
    return np.concatenate((xyz[:,0],xyz[:,-1]))    
def calcFeats2d(xyzs):
    return np.array([calcFeats(xyz) for xyz in xyzs])

def jacobian(thread):
    eps = .1*USCALE
    #t_start = time()
    A,B = thread.clone().makePerts(eps)
    #cprint("makePerts: %.2f"%(time()-t_start))
    Af,Bf = calcFeats2d(A),calcFeats2d(B)
    return (Af-Bf).T/(2*eps[None,:])

def constraint_norm(u):
    """
    norm of under 1 is acceptable
    ok to move by .5, rotate by .25 radians
    """
    return norm(u/USCALE)

def softnormalize(u,d):
    """
    rescale u to have length d
    """
    return u * min(d/constraint_norm(u),1)
