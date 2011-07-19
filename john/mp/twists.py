from __future__ import division
from nibabel.eulerangles import euler2mat,angle_axis2euler,mat2euler
from nibabel.quaternions import angle_axis2mat
import numpy as np
from numpy import arccos,dot,cross,linspace,empty,pi
from numpy.linalg import norm

def twist_around_axis(thread,angle1,angle2,axis):
    xyz = thread.getXYZ()
    cons = thread.getConstraints()    
    mat1 = euler2mat(*cons[3:6])
    mat2 = euler2mat(*cons[9:12])
    tmat1 = euler2mat(*angle_axis2euler(angle1,axis))
    tmat2 = euler2mat(*angle_axis2euler(angle2,axis))    
    newmat1 = dot(tmat1,mat1)
    newmat2 = dot(tmat2,mat2)
    neweul1 = mat2euler(newmat1)
    neweul2 = mat2euler(newmat2)

    cons[3:6] = neweul1
    cons[9:12] = neweul2
    thread.setConstraints(cons)
    
def twist_ctrl(thread,angle1,angle2):
    xyz = thread.getXYZ()
    axis1 = xyz[:,1] - xyz[:,0]
    axis2 = xyz[:,-1] - xyz[:,-2]
    cons = thread.getConstraints()
    mat1 = euler2mat(*cons[3:6])
    mat2 = euler2mat(*cons[9:12])
    tmat1 = euler2mat(*angle_axis2euler(angle1,axis1))
    tmat2 = euler2mat(*angle_axis2euler(angle2,axis2))
    newmat1 = dot(tmat1,mat1)
    newmat2 = dot(tmat2,mat2)
    neweul1 = mat2euler(newmat1)
    neweul2 = mat2euler(newmat2)

    
    #print "orig",cons[blah]
    cons[3:6] = neweul1
    cons[9:12] = neweul2
    thread.setConstraints(cons)
    #print thread.getXYZ()[0]    
    
    #print "set2",cons[blah]
    #print "get2",thread.getConstraints()[blah]

    #print thread.getXYZ()[0]
    
def applyRotVec(x,ang,ax,origin):
    return dot(angle_axis2mat(ang,ax),x-origin[:,None])+origin[:,None]
    
def applyRotEul(eul,ang,ax):
    return mat2euler(dot(angle_axis2mat(-ang,ax),euler2mat(*eul)))
    
def jumprope(thread,ang_rot,ang_conj=.5,n_rot=10,n_conj=3):
    xyz = thread.getXYZ()
    
    tri_inds = [0,1,2]
    p0,p1,p2 = (xyz[:,i] for i in tri_inds)
    ax_normal1 = cross(p1-p0,p2-p0)
    ax_tan1 = p1 - p0

    tri_inds = [-1,-2,-3]
    p0,p1,p2 = (xyz[:,i] for i in tri_inds)
    ax_normal2 = cross(p1-p0,p2-p0)
    ax_tan2 = p1 - p0        
    
    cons = thread.getConstraints()
    eul1 = cons[3:6]
    eul2 = cons[9:12]
    
    for t in xrange(n_conj):
        cons[3:6] = applyRotEul(cons[3:6],ang_conj/n_conj,ax_normal1)
        cons[9:12] = applyRotEul(cons[9:12],ang_conj/n_conj,ax_normal2)
        yield cons
        
    for t in xrange(n_rot):
        cons[3:6] = applyRotEul(cons[3:6],ang_rot/n_rot,ax_tan1)
        cons[9:12] = applyRotEul(cons[9:12],-ang_rot/n_rot,ax_tan2)
        yield cons
        
    for t in xrange(n_conj):
        cons[3:6] = applyRotEul(cons[3:6],-ang_conj/n_conj,ax_normal1)
        cons[9:12] = applyRotEul(cons[9:12],-ang_conj/n_conj,ax_normal2)
        yield cons

def angBetween(vec1,vec2):
    return arccos(dot(vec1,vec2)/norm(vec1)/norm(vec2))
   
def normal_line(xyz):
    mid = xyz.shape[1]//2
    p0,p1,p2 = xyz[:,0],xyz[:,mid],xyz[:,-1]
    return cross(p0-p1,p2-p1)
    

def jumprope2(thread,ang_rot=None,target_thread=None,ang_conj=.5,n_rot=10,n_conj=3):
    xyz = thread.getXYZ()
    
    s0 = xyz[:,0]
    s1 = xyz[:,1]
    e0 = xyz[:,-1]
    e1 = xyz[:,-2]
    
    ax_rot = e0-s0
    
            
    ang_conj1 = ang_conj - angBetween(s1-s0,ax_rot)
    ang_conj2 = ang_conj - angBetween(e0-e1,ax_rot)
    # will fail if angle is greater than pi/2
    
    #ax_norm1 = cross(s1-s0,ax_rot)
    #ax_norm2 = cross(e0-e1,ax_rot)
    ax_norm1 = cross(xyz[:,2]-s0,ax_rot)
    ax_norm2 = cross(e0-xyz[:,-3],ax_rot)
    
    # rotate away from ax_rot
    cons = thread.getConstraints()
    
    for t in xrange(n_conj):
        cons[3:6] = applyRotEul(cons[3:6],ang_conj1/n_conj,ax_norm1)
        cons[9:12] = applyRotEul(cons[9:12],ang_conj2/n_conj,ax_norm2)
        yield cons
    
    dists = [np.inf]
    xyz_targ = target_thread.getXYZ()
    ang_rot = -opt_rot(thread.getXYZ(),target_thread.getXYZ())
    print ang_rot
    for t in xrange(2*n_rot):
        print t
        cons[3:6] = applyRotEul(cons[3:6],ang_rot/n_rot,ax_rot)
        cons[9:12] = applyRotEul(cons[9:12],ang_rot/n_rot,ax_rot)
        yield cons
        dist = norm(thread.getXYZ()-xyz_targ)
        dists.append(dist)
        print dist
        
        if dists[-1] > dists[-2]: break

        

    #xyz = thread.getXYZ()        
    #ang_conj1 = angBetween(xyz[:,1]-xyz[:,0],s1-s0)
    #ang_conj2 = angBetween(xyz[:,1]-xyz[:,0],s1-s0)
    
    #ax_norm1 = cross(xyz[:,1]-xyz[:,0],s1-s0)
    #ax_norm2 = cross(e0-e1,xyz[:,-1]-xyz[:,-2])

        
    #for t in xrange(n_conj):
        #cons[3:6] = applyRotEul(cons[3:6],ang_conj1/n_conj,-ax_norm1)
        #cons[9:12] = applyRotEul(cons[9:12],ang_conj2/n_conj,ax_norm2)
        #yield cons
        


def opt_rot(xyz1,xyz2,n_rot=10):
    ax_rot = xyz1[:,-1] - xyz1[:,0]
    angs_coarse = linspace(0,2*pi,n_rot)
    dists_coarse = [norm(applyRotVec(xyz1,ang,ax_rot,xyz1[:,0])-xyz2)
             for ang in angs_coarse]    
    i_best1,i_best2 = np.argsort(dists_coarse)[:2]
    
    angs_fine = np.linspace(angs_coarse[i_best1],angs_coarse[i_best2],n_rot)
    dists_fine = [norm(applyRotVec(xyz1,ang,ax_rot,xyz1[:,0])-xyz2)
             for ang in angs_fine]

    return angs_fine[np.argmin(dists_fine)]

#def opt_rot2(xyz1,xyz2,n_rot=10):
    #ax_rot = xyz1[:,-1] - xyz1[:,0]
    #angs_coarse = linspace(0,2*pi,n_rot)
    #dists_coarse = [norm(applyRotVec(xyz1,ang,ax_rot,xyz1[:,0])-xyz2)
             #for ang in angs_coarse]    
    #i_best1,i_best2 = np.argsort(dists_coarse)[:2]
    
    #angs_fine = np.linspace(angs_coarse[i_best1],angs_coarse[i_best2],n_rot)
    #dists_fine = [norm(applyRotVec(xyz1,ang,ax_rot,xyz1[:,0])-xyz2)
             #for ang in angs_fine]

    #return angs_fine[np.argmin(dists_fine)]