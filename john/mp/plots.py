import mayavi.mlab as mlab
from numpy import pi,cos,sin,mgrid,array
from mp.utils import normr,colorSeq
from itertools import izip
def plotOrs(*ptss):

    mlab.figure(34); mlab.clf()

    r = 1
    phi, theta = mgrid[0:pi:101j, 0:2*pi:101j]
    
    x = r*sin(phi)*cos(theta)
    y = r*sin(phi)*sin(theta)
    z = r*cos(phi)

    
    mlab.mesh(x,y,z, colormap='gray',opacity=.2)
    
    
    
    colors = [(1,0,0),(0,1,0),(0,0,1)]
    print len(colors)
    print len(ptss)
    for (pts,col) in izip(ptss,colors):
        print col        
        ors = normr(pts)
        # Create a sphere
        
        x,y,z = ors.T
        
        mlab.points3d(x,y,z,color=col)
        mlab.plot3d(x,y,z,color=col,tube_radius=.025)