import enthought.mayavi.mlab as mlab
from numpy.linalg import norm
from numpy import *
from mp.geom import angBetween
from doo.doo import Thread
from mp.utils import upsample2D,normr,almostEq,ndinterp,colorSeq
from simplectrl2 import getState,setOrs,applyTwist,infTwist
import plots

mlab.clf()
if __name__ == "__main__":
    
    colors = colorSeq(100)
    T = 30
    
    center = r_[0,0,0]
    mainax = r_[10,0,0]
    up = r_[0,0,1]
    elev = pi/3
    thread = Thread()
    
    
    
    x,y,z = xyz = thread.getXYZ()
    
    p1_arch = center - mainax
    p2_arch = center + mainax        
    v1_arch = normr(mainax + normr(up)*norm(mainax)*tan(elev))
    v2_arch = normr(mainax - normr(up)*norm(mainax)*tan(elev))
    
    p1_now,v1_now,p2_now,v2_now = getState(thread)    
    
    p1s = upsample2D(array([p1_now,p1_arch]),T,1)
    p2s = upsample2D(array([p2_now,p2_arch]),T,1)    
    v1s = upsample2D(array([v1_now,v1_arch]),T,1)
    v2s = upsample2D(array([v2_now,v2_arch]),T,1)
    
    for (p1,p2,v1,v2) in zip(p1s,p2s,v1s,v2s):
        col = colors.next()

        setOrs(thread,p1,v1,p2,v2)
        x,y,z = thread.getXYZ()
        mlab.plot3d(x,y,z,tube_radius=.15,color=col)

        x,y,z = c_[p1,p1+3*v1]        
        mlab.plot3d(x,y,z,tube_radius=.3,color=col)
        x,y,z = c_[p2,p2+3*v2]        
        mlab.plot3d(x,y,z,tube_radius=.3,color=col)
    
    for _ in xrange(20): col = colors.next()
    
    for dtwist in [.1,-.1]:
        for t in xrange(25):
            col = colors.next()
            applyTwist(thread,dtwist,0)
            xyz=x,y,z = thread.getXYZ()        
            mlab.plot3d(x,y,z,tube_radius=.15,color=col)
            print "t,inf twist:",t,infTwist(xyz)
    
    #pts = xyz.T
    #ors = normr(pts[1:] - pts[:-1])
    #plots.plotOrs(ors)

    #print "p_start,p_end",p_start,p_end
    
    #while True:
        #xyz = thread.getXYZ()
        #s0 = xyz.T[0]
        #e0 = xyz.T[-1]
        
    
    #while True:
        #xyz = thread.getXYZ()
        #s0,s1,e1,e0 = xyz.T[[0,1,-2,-1]]
        #print "s0,e0",s0,e0
        #print "ang_start",angBetween(v_start,s1-s0)
        #print "ang_end",angBetween(v_end,e0-e1)
        #if almostEq(s0,p_start) and almostEq(e0,p_end) and\
           #almostEq(v_start,s1-s0) and almostEq(v_end,e0-e1): break
        #else:
            #t_start = trunc(p_end - s0,.5)
            #t_end = trunc(p_start - e0,.5)
            ##print t_start,t_end
            #ang1 = trunc(angBetween(v_start,s1-s0),.05)
            #ang2 = trunc(angBetween(v_end,e0-e1),.05)
            #cons = moveEndCons(thread,t_start,t_end,"towards",(v_start,ang1),(v_end,ang2))
            ##cons = thread.getConstraints()
            ##cons = r_[cons[0:3]+t_start,cons[3:6],cons[6:9]+t_end,cons[9:12]]
        