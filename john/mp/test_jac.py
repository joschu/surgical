from pylab import *
from doo import Thread
from control import jacobian,calcFeats2d
from settings import *
import numpy as np
from utils import upsample2D

thread = Thread()
#A,B = thread.makePerts()
scale = .25
cons_start = thread.getConstraints()
cons_1 = cons_start + scale*r_[randn(3)*10,randn(3)*.5,randn(3)*10,randn(3)*.5]
cons_2 = cons_start + scale*r_[randn(3)*10,randn(3)*.5,randn(3)*10,randn(3)*.5]
cons_end = cons_start + scale*r_[randn(3)*10,randn(3)*.5,randn(3)*10,randn(3)*.5]
for i,cons in enumerate(upsample2D(np.array([cons_start,cons_1,cons_2,cons_end]),80)):
    print i
    thread.setConstraints(cons)


q = thread.getXYZ()

#print "linear approx":
for a in xrange(12):
    eps = zeros(12)
    eps[a] = USCALE[a]
    steps = linspace(-1,1,20)
    perts = outer(steps,eps)
    con = thread.getConstraints()
    xyzs = []
    for pert in perts:
        t = thread.clone()
        t.setConstraints(con+pert)
        xyzs.append(t.getXYZ().flatten())
    xyzs = array(xyzs)
    cxyzs = xyzs - xyzs.mean(axis=0)
    figure(a)
    plot(steps,cxyzs)
