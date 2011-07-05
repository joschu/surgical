from doo.doo import Thread
from comm import readMats,writeMats
from time import sleep,time
import numpy as np
#t = Thread()
#t.printVertices()
#t.dump()

def test_load():
    t = Thread()
    print "before:"
    t.printVertices()
    t.load(np.random.randn(3,11),2)
    print "after:"
    t.printVertices()
    
def test_load2():
    t1 = Thread()
    t1.load(np.random.randn(3,11),2)
    xyz = t1.getXYZ()        
    
    t2 = Thread()
    t2.load(xyz,0)
    
    t1.minimizeEnergy()
    xyz1 = t1.getXYZ()
    t2.minimizeEnergy()
    xyz2 = t2.getXYZ()
    
    print xyz1-xyz2
    
if __name__ == "__main__":
    test_load()
    test_load2()