import doo
from doo.dooview import MlabGui
from linearization import *

start_thread = Thread()
goal_thread = Thread()

cons = start_thread.getConstraints()
cons[0] += 10 # start x
cons[6] += 10 # end x

goal_thread.setConstraints(cons)

xyz_start = start_thread.getXYZ()
#start_plot = mlab.plot3d(xyz_start[0],xyz_start[1],xyz_start[2],tube_radius=.5,color=(1,0,0))

xyz_goal = goal_thread.getXYZ()
#goal_plot = mlab.plot3d(xyz_goal[0],xyz_goal[1],xyz_goal[2],tube_radius=.5,color=(0,0,1))

#cur_plot = mlab.plot3d(xyz_start[0],xyz_start[1],xyz_start[2],tube_radius=.5,color=(0,1,0))

goal_state = calcFeats(xyz_goal.flatten())    
xyzs = [xyz_start]
for i in xrange(100):
    print "iteration",i
    J = jacobian(start_thread)
    xyz_cur = start_thread.getXYZ()
    cur_state = calcFeats(xyz_cur.flatten())
    step = np.dot(J.T,goal_state - cur_state)
    print "step:",step
    old_cons = start_thread.getConstraints()
    new_cons = old_cons + softnormalize(step,.4)
    tstart = time()
    start_thread.setConstraints(new_cons)
    cprint("setconstraints time: %.2f"%(time()-tstart),"red")
    xyzs.append(xyz_cur)
    #mlab.plot3d(xyz_cur[0],xyz_cur[1],xyz_cur[2],color=(1,0,0))
    
class fb:
    i = 0
    def __init__(self,xyzs):
        self.xyzs = xyzs
        self.gui = MlabGui([self.back,self.fwd])
        self.mlab = self.gui.scene.mlab
        opts = dict(tube_radius=.5)
        xyz_start = xyzs[0]
        xyz_end = xyzs[-1]
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
        x,y,z = self.xyzs[self.i]            
        self.plot_cur.mlab_source.set(x=x,y=y,z=z)
        print "updated to %i"%self.i
    def start(self):
        self.gui.configure_traits()
        
fb().start()