import mayavi.mlab as mlab
import numpy as np
from nibabel.quaternions import angle_axis2mat

x,y,z = xyz = np.load("xyz.npy")
# orig line
mlab.clf()
mlab.plot3d(x,y,z,color=(1,0,0),tube_radius=.1)
# fit quads to both ends

tri_inds = [0,1,2]
theta = .5
p0,p1,p2 = (xyz[:,i] for i in tri_inds)
ax_normal = np.cross(p1-p0,p2-p0)
ax_tan = p1 - p0
ax_rot = np.dot(angle_axis2mat(theta,ax_normal),ax_tan)

t = np.linspace(-2,2,30)
for ax in ax_normal,ax_tan,ax_rot:
    x,y,z = p0[:,None] + ax[:,None]*t[None,:]
    mlab.plot3d(x,y,z,color=(0,1,0),tube_radius=.1)