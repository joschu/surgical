cdef extern from "thread_discrete.h":
    cdef cppclass Thread:
        Thread()
        void print_vertices()
        
cdef class PyThread:
    cdef Thread *thisptr
    def __cinit__(self):
        self.thisptr = new Thread()
    def __dealloc(self):
        del self.thisptr
    def print_vertices(self):
        self.thisptr.print_vertices()
        
print "hi"
pt = PyThread()
pt.print_vertices()
del pt
