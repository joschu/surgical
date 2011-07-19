from numpy import cross
from utils import normr

def twistArea(xyz):
    assert xyz.shape[1] >= 4
    p0 = xyz.T[0]
    dirs = normr(xyz.T[1:] - xyz.T[:-1])
    diffs = cross(dirs[2:]-p0,dirs[1:-1]-p0)
    rads = normr(dirs[1:-1]+dirs[2:]+p0[None,:])
    areas = (diffs*rads).sum(axis=1)
    return .5*areas.sum()
