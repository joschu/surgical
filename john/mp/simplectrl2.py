#from doo.doo import Thread2
from mp.utils import normr,almostEq
from mp.geom import angBetween
from numpy import eye,dot,diag,cross,zeros
from numpy.random import randn
import logging; L = logging.Logger(__file__)
L.setLevel(logging.DEBUG)
from nibabel.quaternions import angle_axis2mat,mat2quat,quat2angle_axis

def getState(thread):
    "get position and orientation of ends"
    xyz = thread.getXYZ()
    s0,s1,e1,e0 = xyz.T[[0,1,-2,-1]]
    return s0,normr(s1-s0),e0,normr(e0-e1)
    
def setOrs(thread,pos1,or1,pos2,or2):
    "set orientation of ends"
    old_pos1,old_or1,old_pos2,old_or2 = getState(thread)
    thread.applyMotion(pos1-old_pos1,minRot(or1,old_or1),
                       pos2-old_pos2,minRot(or2,old_or2))

def applyTwist(thread,twist1,twist2):
    "twist the ends"
    _,or1,_,or2 = getState(thread)
    thread.applyMotion(zeros(3),angle_axis2mat(twist1,or1),zeros(3),angle_axis2mat(twist2,or2))
    
def minRot(ax1,ax2):
    "find the rotation matrix that takes ax1 to ax2"
    if almostEq(ax1,ax2):
        L.debug("minRot: same vector")
        return eye(3)
    elif almostEq(ax1,-ax2):
        L.debug("minRot: opp vector")
        return -diag([-1,-1,0])
    else:
        ax_rot = cross(ax2,ax1)
        return angle_axis2mat(angBetween(ax1,ax2),ax_rot)
    
def infTwist(xyz):
    pts = xyz.T
    ors = normr(pts[1:] - pts[:-1])
    
    start2end_rope = eye(3)
    for (or1,or2) in zip(ors[:-1],ors[1:]):
        start2end_rope = dot(minRot(or2,or1),start2end_rope)
    
    assert almostEq(dot(start2end_rope,ors[0]),ors[-1])
    end2start_min = minRot(ors[0],ors[-1])
    
    twist_mat = dot(end2start_min,start2end_rope)
    ang,_ = quat2angle_axis(mat2quat(twist_mat))
    return ang

def test_infTwist():
    xyz = randn(3,100)
    infTwist(xyz)
    
def test_minRot():
    for _ in xrange(100):
        x1 = normr(randn(3))
        x2 = normr(randn(3))
        assert almostEq(x1,dot(minRot(x1,x2),x2))
        

if __name__ == "__main__":
    test_minRot()
    test_infTwist()