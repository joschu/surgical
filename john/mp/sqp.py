from doo import *
from linearization import calcFeats,jacobian
from utils import ndinterp,cprint
from Wormhole import Wormhole
from doo.dooview import fb

matlab = None

def frPath(start_thread,goal_thread,T,s_t = None):    
    global matlab
    matlab = Wormhole()      

    # generate a sequence of fantasy states Sf
    # minimize energy to get Sr
    # calculate jacobians
    # solve linear prob for changes in u
    
    #s_start = calcFeats(start_thread.getXYZ().flatten())
    s_start = start_thread.getConstraints()
    #s_goal = calcFeats(goal_thread.getXYZ().flatten())    
    s_goal = goal_thread.getConstraints()
    
    #s_t = ndinterp(linspace(0,1,T),np.r_[s_start,s_goal],[0,1])
    if s_t is None: s_t = ndinterp(np.linspace(0,1,T),[0,1],np.array([s_start,s_goal]))

    #import mayavi.mlab as mlab
    for i in xrange(10):
        
        #fwd_states1,_ = calcStatesJacs(start_thread,s_t)
        #fwd_states2 = calcStates(start_thread,s_t)
        #print np.linalg.norm(fwd_states1-fwd_states2)

        #rev_states1,_ = calcStatesJacs(goal_thread,s_t[::-1])
        #rev_states2 = calcStates(goal_thread,s_t[::-1])
        #print np.linalg.norm(rev_states1-rev_states2)
        
        
        print "forwards"
        fwd_states,fwd_jacs = calcStatesJacs(start_thread,s_t)
        print "backwards"
        rev_states,rev_jacs = [li[::-1] for li in calcStatesJacs(goal_thread,s_t[::-1])]
        #fwd_jacs = [jacobian(state) for state in fwd_states]
        #rev_jacs = [jacobian(state) for state in rev_states]
        #mlab.clf()
        #for s in fwd_states:
            #x,y,z = s.reshape(3,-1)
            #mlab.plot3d(x,y,z,tube_radius=.1,color=(1,0,0))   
            #mlab.points3d(x[[0,-1]],y[[0,-1]],z[[0,-1]],.5*np.ones(2),scale_factor=1,color=(1,1,1))
        #mlab.show()
        
        diff_states = fwd_states - rev_states
        #print "diff", evalDiff(start_thread,goal_thread,s_t)                
        
        cprint("states diff: %.2f"%np.linalg.norm(diff_states),"blue")
        cprint("jac diff: %.2f"%np.linalg.norm((fwd_jacs - rev_jacs).flatten()),"blue")
        cprint("end error: %.2ef"%np.linalg.norm(diff_states[-1]),"blue")
        #ds_t = frLinear(diff_states,fwd_jacs,rev_jacs)
        ds_t = frLinear2(diff_states,fwd_jacs - rev_jacs,s_t)
        step_sizes = np.array([-.5,-.1,.01,.1,.5,1])
        dists = [evalDiff(start_thread,goal_thread,s_t+step*ds_t) for step in step_sizes]
        print "dists",dists
        best_step = step_sizes[np.argmin(dists)]
        s_t += best_step*ds_t
        print "best step",best_step
        if i in [0,9]: fb(fwd_states.reshape(T,3,-1),goal_thread.getXYZ()).start()
        #print "dists:",dists
                
        

    
def calcStatesJacs(thread,u_t):
    thread = thread.clone()
    states = [calcFeats(thread.getXYZ().flatten())]
    jacs = [jacobian(thread)]
    for u in u_t[1:]:
        thread.setConstraints(u)
        states.append(calcFeats(thread.getXYZ().flatten()))
        jacs.append(jacobian(thread.clone()))
    return np.array(states),np.array(jacs)

def calcStates(thread,u_t):
    thread = thread.clone()
    states = [calcFeats(thread.getXYZ().flatten())]
    for u in u_t[1:]:
        thread.setConstraints(u)
        states.append(calcFeats(thread.getXYZ().flatten()))
    return np.array(states)

def evalDiff(start_thread,goal_thread,u_t):
    return np.linalg.norm(calcStates(start_thread,u_t) - calcStates(goal_thread,u_t[::-1])[::-1])

def frLinear(diff_states,fwd_jacs,rev_jacs):
    matlab.put("diff_states",diff_states)
    matlab.put("fwd_jacs",fwd_jacs)
    matlab.put("rev_jacs",rev_jacs)
    matlab.execute("du = frLinear(diff_states,fwd_jacs,rev_jacs)")
    du_t = matlab.get("du").T
    ds_t = np.r_[np.zeros((1,du_t.shape[1])),np.cumsum(du_t,axis=0)]    
    return ds_t

def frLinear2(diff_states,diff_jacs,s_t):
    matlab.put("diff_states",diff_states)
    matlab.put("diff_jacs",diff_jacs)
    matlab.put("s_t",s_t.T)
    matlab.execute("ds = frLinear2(diff_states,diff_jacs,s_t)")
    K = diff_jacs.shape[2]
    ds_t = np.r_[np.zeros((1,K)),matlab.get("ds").T,np.zeros((1,K))]
    return ds_t


def linearProb(Sstart,Sgoal,Js,T):
    """
    Sstart, Sgoal: (N,)
    Js: (T-1,N,K)
    """
    pass
