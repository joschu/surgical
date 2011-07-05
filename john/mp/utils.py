import numpy as np
from numpy.linalg import norm
from scipy.interpolate import splrep,splev
from itertools import cycle

color_seqs = dict(
    purple = '\033[95m',
    blue = '\033[94m',
    green = '\033[92m',
    yellow = '\033[93m',
    red = '\033[91m',
    end = '\033[0m')
    
def cprint(string,color="red"):
    print(color_seqs[color]+string+color_seqs["end"])

def upsample1D(y,T):
    x = np.linspace(0,1,y.size)
    xnew = np.linspace(0,1,T)
    tck = splrep(x,y,k=min(len(x)-1,3))
    return splev(xnew,tck)

def upsample2D(y,T):
    "upsample y along axis 0"
    return np.array([upsample1D(ycol,T) for ycol in y.T]).T

def ndinterp(x,xp,yp):
    """n-dimensional interpolation
    Same interface as np.interp, except yp can be n-dimensional"""
    xp,yp = np.asarray(xp),np.asarray(yp)
    ind = np.interp(x,xp,np.arange(len(xp)))
    intpart = np.clip(np.int32(np.trunc(ind)),0,yp.shape[0]-2)
    fracpart = ind - intpart
    shape = (-1,) + (1,)*(yp.ndim-1)
    return (1-fracpart).reshape(*shape)*yp[intpart]+ fracpart.reshape(*shape)*yp[intpart+1]

def colorSeq(N):
    colors =  ndinterp(np.linspace(0,1,N),np.linspace(0,1,7),
                       np.array([[0,0,1],[0,1,0],[0,1,1],
                                 [1,0,0],[1,0,1],[1,1,0],[1,1,1]]))
    for col in cycle(colors): yield tuple(col)

def trunc(x,p):
    x1 = x.copy()
    toobig = abs(x1) > p
    x1[toobig] = (p*np.sign(x1))[toobig]
    return x1