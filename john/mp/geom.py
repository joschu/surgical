from nibabel.eulerangles import euler2mat,angle_axis2euler,mat2euler
from nibabel.quaternions import angle_axis2mat
from numpy import dot,arccos
from numpy.linalg import norm

def applyRotEul(eul,ang,ax):
    "compose a rotation of ang around ax with rotation given by euler angles eul"
    return mat2euler(dot(angle_axis2mat(ang,ax),euler2mat(*eul)))

def applyRotVec(x,ang,ax,origin):
    "rotate a vector x by ang around axis defined by ray origin+ax"
    return dot(angle_axis2mat(ang,ax),x-origin[:,None])+origin[:,None]

def angBetween(vec1,vec2):
    "angle between vectors, in range [0,pi]"
    return arccos(dot(vec1,vec2)/norm(vec1)/norm(vec2))
    