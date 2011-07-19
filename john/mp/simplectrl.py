from doo import USCALE
import numpy as np
from numpy import pi,dot,cross,tan,r_
from numpy.linalg import norm
from nibabel.eulerangles import euler2mat,angle_axis2euler,mat2euler
from nibabel.quaternions import angle_axis2mat
from mp.utils import almostEq,normr,trunc
from mp.geom import angBetween


def moveEndCons(thread,trans1,trans2,rot_type,rot1,rot2):
    cons = thread.getConstraints()
    eulnew1 = transformEuler(cons[3:6],rot_type,rot1)
    eulnew2 = transformEuler(cons[9:12],rot_type,rot2)
    
    return np.r_[cons[0:3]+trans1,eulnew1,cons[6:9] + trans2, eulnew2]

def transformEuler(eul1,rot_type,rot):
    mat1 = euler2mat(*eul1)

    if rot_type == "angle_axis":
        ang1,ax1 = rot
        tmat1 = angle_axis2mat(ax1,ang1)
    elif rot_type == "mat":
        tmat1 = rot
    elif rot_type == "euler":
        eul1 = rot
        tmat1 = euler2mat(*eul1)
    elif rot_type == "towards":
        targ_vec1,ang1 = rot
        cur_vec1 = euler2mat(*eul1)[:,0]
        ax_rot1 = cross(cur_vec1,targ_vec1)
        tmat1 = angle_axis2mat(ang1,ax_rot1)
    else: raise Exception("rotation type %s not understood"%rot_type)
    mat1new = dot(tmat1,mat1)
    return mat2euler(mat1new)

def makeArch(thread, center, mainax, up, elev):
    p_start = center - mainax
    p_end = center + mainax        
    v_start = normr(mainax + normr(up)*norm(mainax)*tan(elev))
    v_end = normr(mainax - normr(up)*norm(mainax)*tan(elev))
    
    print "p_start,p_end",p_start,p_end
    
    while True:
        xyz = thread.getXYZ()
        s0 = xyz.T[0]
        e0 = xyz.T[-1]
        
    
    while True:
        xyz = thread.getXYZ()
        s0,s1,e1,e0 = xyz.T[[0,1,-2,-1]]
        print "s0,e0",s0,e0
        print "ang_start",angBetween(v_start,s1-s0)
        print "ang_end",angBetween(v_end,e0-e1)
        if almostEq(s0,p_start) and almostEq(e0,p_end) and\
           almostEq(v_start,s1-s0) and almostEq(v_end,e0-e1): break
        else:
            t_start = trunc(p_end - s0,.5)
            t_end = trunc(p_start - e0,.5)
            #print t_start,t_end
            ang1 = trunc(angBetween(v_start,s1-s0),.05)
            ang2 = trunc(angBetween(v_end,e0-e1),.05)
            cons = moveEndCons(thread,t_start,t_end,"towards",(v_start,ang1),(v_end,ang2))
            #cons = thread.getConstraints()
            #cons = r_[cons[0:3]+t_start,cons[3:6],cons[6:9]+t_end,cons[9:12]]
            yield cons            
            
if __name__ == "__main__":
    from numpy import r_
    transformEuler(r_[0,0,0],"angle_axis",(r_[0,0,1],pi/2))
        