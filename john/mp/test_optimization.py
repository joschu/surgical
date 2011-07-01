import scipy.optimize as opt
from pylab import *
from time import time

from settings import *
from doo import Thread
from sqp import frPath,calcStates,evalDiff
from numpy.random import randn
from utils import upsample2D

T = 15
start_thread = Thread()
scale=.25
cons_start = start_thread.getConstraints()

n_wp = 1

def randCons(n): return cons_start + scale*USCALE[None,:]*randn(n,12)

cons_end = randCons(1)
def makeTraj(cons_mid):
    cons_t = upsample2D(np.r_[
            atleast_2d(cons_start),
            atleast_2d(cons_mid),
            atleast_2d(cons_end)],T)
    return cons_t
    
def flattenWP(cons_t): return cons_t.flatten()
def unflattenWP(x): return x.reshape(-1,12)

goal_thread = start_thread.clone()
t_start = time()
for cons in makeTraj(randCons(1)):
    goal_thread.setConstraints(cons)
print "time:",t_start-time()

def sayhi(_): print "hi"

x0 = flattenWP(upsample2D(np.array([cons_start.flatten(),cons_end.flatten()]),n_wp+2)[1:-1])


def totalCost(start_thread,goal_thread,s_t,alpha=1000):
    move_cost = alpha*(s_t[1:] - s_t[:-1]).max()
    diff_cost = evalDiff(start_thread,goal_thread,s_t)
    return move_cost + diff_cost

print "before",totalCost(start_thread,goal_thread,makeTraj(unflattenWP(x0)),0)
xopt=opt.fmin(lambda x: totalCost(start_thread,goal_thread,makeTraj(unflattenWP(x)),0),
         x0=x0,ftol=.1,disp=2)
print "after",totalCost(start_thread,goal_thread,makeTraj(unflattenWP(xopt)),0)
#print evalDiff(start_thread,goal_thread,cons_t)

