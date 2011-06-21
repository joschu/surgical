from __future__ import division
from dooview import MlabGui
from doo import GLThread
import numpy as np
from time import sleep,time
from utils import cprint
from logging import Logger
from numpy.linalg import norm

L = Logger


def calcFeats(xyzFlat):
    xyz = xyzFlat.reshape(3,-1)
    return np.concatenate((xyz[:,0],xyz[:,-1]))    
def calcFeats2d(xyzs):
    return np.array([calcFeats(xyz) for xyz in xyzs])

def jacobian(thread):
    eps = 1e-2
    #t_start = time()
    A,B = thread.makePerts(eps)
    #cprint("makePerts: %.2f"%(time()-t_start))
    Af,Bf = calcFeats2d(A),calcFeats2d(B)
    return (Af-Bf).T/eps

def constraint_norm(u):
    """
    norm of under 1 is acceptable
    ok to move by .5, rotate by .25 radians
    """
    move1,rot1,move2,rot2 = u.reshape(4,3)
    return max(norm(move1)/.5,norm(move2)/.5,norm(rot1)/.25,norm(rot2)/.25)

def rescale(u,d):
    """
    rescale u to have length d
    """
    return d * u / (constraint_norm(u)+1e-3)

if __name__ == "__main__":
    start_thread = GLThread()
    goal_thread = GLThread()

    cons = start_thread.getConstraints()
    cons[0] += 10 # start x
    cons[6] += 10 # end x
    
    goal_thread.setConstraints(cons)
    
    xyz_start = start_thread.getXYZ()
    #start_plot = mlab.plot3d(xyz_start[0],xyz_start[1],xyz_start[2],tube_radius=.5,color=(1,0,0))
    
    xyz_goal = goal_thread.getXYZ()
    #goal_plot = mlab.plot3d(xyz_goal[0],xyz_goal[1],xyz_goal[2],tube_radius=.5,color=(0,0,1))
    
    #cur_plot = mlab.plot3d(xyz_start[0],xyz_start[1],xyz_start[2],tube_radius=.5,color=(0,1,0))

    goal_state = calcFeats(xyz_goal)    
    xyzs = []
    for i in xrange(100):
        print "iteration",i
        J = jacobian(start_thread)
        xyz_cur = start_thread.getXYZ()
        cur_state = calcFeats(xyz_cur.flatten())
        step = np.dot(J.T,goal_state - cur_state)
        print "step:",step
        old_cons = start_thread.getConstraints()
        new_cons = old_cons + rescale(step,.4)
        tstart = time()
        start_thread.setConstraints(new_cons)
        cprint("setconstraints time: %.2f"%(time()-tstart),"red")
        xyzs.append(xyz_cur)
        
    class fb:
        i = 0
        def __init__(self):
            self.gui = MlabGui([self.back,self.fwd])
            self.mlab = self.gui.scene.mlab
            opts = dict(tube_radius=.5)
            
            self.mlab.plot3d(
                xyz_start[0],xyz_start[1],xyz_start[2],color=(1,0,0),**opts)
            self.plot_cur = self.mlab.plot3d(
                xyz_start[0],xyz_start[1],xyz_start[2],color=(0,1,0),**opts)
            self.mlab.plot3d(
                xyz_goal[0],xyz_goal[1],xyz_goal[2],color=(0,0,1),**opts)
            
        def fwd(self):
            self.i = min(self.i+1,len(xyzs)-1)
            self.update()
        def back(self):
            self.i = max(self.i-1,0)
            self.update()
        def update(self):
            x,y,z = xyzs[self.i]            
            self.plot_cur.mlab_source.set(x=x,y=y,z=z)
            print "updated to %i"%self.i
        def start(self):
            self.gui.configure_traits()
            
    fb().start()
    