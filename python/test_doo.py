from doo import Thread,GLThread

#t = Thread()
#t.printVertices()
#t.dump()

glt = GLThread()
glt.printThreadData()
glt.minimizeEnergy()
glt.printThreadData()
glt.updateThreadPoints()
glt.printThreadData()
glt.dump()