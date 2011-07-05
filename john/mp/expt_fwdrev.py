from doo import *
from doo.doo import Thread
from sqp import frPath,calcStates,evalDiff
from numpy.random import randn
from utils import upsample2D

T = 30
start_thread = Thread()
scale=.2

cons_start = start_thread.getConstraints()
cons_1 = cons_start + scale*USCALE*randn(12)
cons_2 = cons_start + scale*USCALE*randn(12)
cons_end = cons_start + scale*USCALE*randn(12)

print "moving thread to config 1 so it's hopefully stable"
cons_t = upsample2D(np.array([cons_start,cons_1]),T)
for cons in cons_t:
    start_thread.setConstraints(cons)

    
print "moving it along path 1->2->goal"    
goal_thread = start_thread.clone()
cons_t = upsample2D(np.array([cons_1,cons_2,cons_end]),T)
for cons in cons_t[1:]:
    goal_thread.setConstraints(cons)
    
#print evalDiff(start_thread,goal_thread,cons_t)
frPath(start_thread,goal_thread,T,None)
