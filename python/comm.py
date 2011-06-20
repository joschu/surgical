import numpy as np

def readMats(n):
    return [np.loadtxt("/tmp/matrix%i"%i,skiprows=1) for i in xrange(n)]

def writeMats(*mats):
    for (i,mat) in enumerate(mats):
        mat = np.atleast_2d(mat) 
        assert mat.ndim == 2
        with open("/tmp/matrix%i"%i,"w") as fd:
            fd.write("%i %i\n"%mat.shape)
            np.savetxt(fd,mat,fmt="%.4f")
