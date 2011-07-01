import settings
from dooview import MlabGui
from control import *
from numpy.random import randn
from utils import upsample2D


## Copied from test_path_dependence.py
np.random.seed(1)
scale = .25
T = 10

thread_start = Thread()
n_clones = 3
threads = [thread_start.clone() for _ in xrange(n_clones)]

cons_start = thread_start.getConstraints()
cons_end = cons_start + scale*np.r_[randn(3)*10,randn(3)*.5,randn(3)*10,randn(3)*.5]

x,y,z = thread_start.getXYZ()

for (i,thread) in zip(xrange(n_clones),threads):
    print "thread",i
    cons_mid = cons_start + scale*np.r_[randn(3)*10,randn(3)*.5,randn(3)*10,randn(3)*.5]
    cons_t = upsample2D(np.array([cons_start,cons_mid,cons_end]),T)
    thread = threads[i]
    for (t,cons) in enumerate(cons_t):
        print t
        thread.setConstraints(cons)
        x,y,z = threads[i].getXYZ()
        if t==T-1: tube_radius = .4
        else: tube_radius = .1
        #mlab.plot3d(x,y,z,color=color,tube_radius=tube_radius)

        

start_thread = threads[1]
goal_thread = threads[2]


xyz_start = start_thread.getXYZ()

xyz_goal = goal_thread.getXYZ()
goal_state = calcFeats(xyz_goal.flatten())    
xyzs = [xyz_start]
for i in xrange(200):
    print "iteration",i
    J = jacobian(start_thread)
    xyz_cur = start_thread.getXYZ()
    cur_state = calcFeats(xyz_cur.flatten())
    step = np.dot(J.T,goal_state - cur_state)
    print "step:",step
    old_cons = start_thread.getConstraints()
    new_cons = old_cons + softnormalize(step,.2)
    tstart = time()
    start_thread.setConstraints(new_cons)
    cprint("setconstraints time: %.2f"%(time()-tstart),"blue")
    xyzs.append(xyz_cur)
    #mlab.plot3d(xyz_cur[0],xyz_cur[1],xyz_cur[2],color=(1,0,0))
    
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