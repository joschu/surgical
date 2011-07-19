#from doo import *
from settings import *
import numpy as np
from numpy import dot
from numpy.linalg import norm
from libcpp.vector cimport vector
from comm import readMats,writeMats
from nibabel.eulerangles import euler2mat, mat2euler


cdef extern from "thread_discrete.h":
    cdef cppclass ThreadPiece:
        pass

    cdef cppclass c_Thread "Thread":
        Thread()
        void print_vertices()
        void minimize_energy(int)
        int num_pieces()
        void save_thread_pieces_and_resize(vector[ThreadPiece*] thread_backup_pieces)
        void restore_thread_pieces(vector[ThreadPiece*] thread_backup_pieces)
        
        
cdef extern from "glThread.h":
    cdef cppclass c_GLThread "GLThread":
        GLThread()
        void printThreadData()
        void updateThreadPoints()
        c_Thread* getThread()
        c_Thread* _thread

cdef extern from "communication.h":
    void dumpThread(c_Thread*)
    void loadThread(c_Thread*)
    void loadConstraints(c_Thread*)
        
cdef class Thread:
    cdef c_Thread *thisptr
    def __cinit__(self):
        cdef c_GLThread* glt = new c_GLThread()
        self.thisptr = glt.getThread()
        self.minimizeEnergy()
    def printVertices(self):
        self.thisptr.print_vertices()
    def dump(self):
        dumpThread(self.thisptr)
    def load(self,xyz,twist):
        """xyz : 3xN array
        twist: scalar"""
        vec = np.append(xyz.flatten(),twist)
        writeMats(vec)
        loadThread(self.thisptr)                
    def minimizeEnergy(self,n_iter = 1000):
        self.thisptr.minimize_energy(n_iter)
    def setConstraints(self,c):
        start,start_ang,end,end_ang = c[0:3],c[3:6],c[6:9],c[9:12]
        writeMats(start,euler2mat(*start_ang),end,euler2mat(*end_ang))
        self.loadConstraints()        
        self.minimizeEnergy()
    def loadConstraints(self):
        loadConstraints(self.thisptr)
    def getXYZ(self):
        dumpThread(self.thisptr)
        return readMats(1)[0]
    def getData(self):
        dumpThread(self.thisptr)
        return readMats(3)
    def getConstraints(self):
        xyz,start_rot,end_rot = self.getData()
        start,end = xyz[:,0],xyz[:,-1]
        return np.r_[start,mat2euler(start_rot),end,mat2euler(end_rot)]
    def makePerts(self,eps=None):
        if eps is None: eps = .1*USCALE
        n_ctl = 12
        n_seg = self.thisptr.num_pieces()
        cdef vector[ThreadPiece*] thread_backup_pieces 
        self.thisptr.save_thread_pieces_and_resize(thread_backup_pieces)
        u = self.getConstraints()
        A = np.zeros((n_ctl,3*n_seg))
        B = np.zeros((n_ctl,3*n_seg))
                
        for i_pert in xrange(12):
            du = np.zeros(12)                        
            du[i_pert] = eps[i_pert]
            
            self.setConstraints(u + du)
            A[i_pert] = self.getXYZ().flatten()
            self.thisptr.restore_thread_pieces(thread_backup_pieces)
            
            self.setConstraints(u - du)
            B[i_pert] = self.getXYZ().flatten()
            self.thisptr.restore_thread_pieces(thread_backup_pieces)
        return A,B
    def clone(self):
        cdef vector[ThreadPiece*] thread_backup_pieces 
        self.thisptr.save_thread_pieces_and_resize(thread_backup_pieces)
        bro = Thread()
        bro.thisptr.restore_thread_pieces(thread_backup_pieces)
        return bro
    def applyMotion(self,move1,rot1,move2,rot2):
        xyz,mat1,mat2 = self.getData()    
        writeMats(xyz[:,0]+move1,dot(rot1,mat1),xyz[:,-1]+move2,dot(rot2,mat2))
        self.loadConstraints()        
        self.minimizeEnergy()
  
cdef class GLThread:
    cdef c_GLThread *thisptr
    cdef c_Thread *threadptr
    def __cinit__(self):
        self.thisptr = new c_GLThread()
        cdef c_Thread* threadptr = self.thisptr.getThread()
        self.threadptr = threadptr
        self.minimizeEnergy()
    def __dealloc(self):
        del self.thisptr
    def minimizeEnergy(self):
        self.threadptr.minimize_energy(1000)
    def printThreadData(self):
        self.thisptr.printThreadData()
    def updateThreadPoints(self):
        self.thisptr.updateThreadPoints()
    def dump(self):
        dumpThread(self.threadptr)
    def setConstraints(self,c):
        start,start_ang,end,end_ang = c[0:3],c[3:6],c[6:9],c[9:12]
        writeMats(start,euler2mat(*start_ang),end,euler2mat(*end_ang))
        self.loadConstraints()        
        self.minimizeEnergy()
    def loadConstraints(self):
        loadConstraints(self.threadptr)
    def getXYZ(self):
        dumpThread(self.threadptr)
        return readMats(1)[0]
    def getData(self):
        dumpThread(self.threadptr)
        return readMats(3)
    def getConstraints(self):
        xyz,start_rot,end_rot = self.getData()
        start,end = xyz[:,0],xyz[:,-1]
        return np.r_[start,mat2euler(start_rot),end,mat2euler(end_rot)]
    def makePerts(self,eps=None):
        if eps is None: eps = .1 * USCALE
        n_ctl = 12
        n_seg = self.threadptr.num_pieces()
        cdef vector[ThreadPiece*] thread_backup_pieces 
        self.threadptr.save_thread_pieces_and_resize(thread_backup_pieces)
        u = self.getConstraints()
        A = np.zeros((n_ctl,3*n_seg))
        B = np.zeros((n_ctl,3*n_seg))
                
        for i_pert in xrange(12):
            du = np.zeros(12)                        
            du[i_pert] = eps[i_pert]
            
            self.setConstraints(u + du)
            A[i_pert] = self.getXYZ().flatten()
            self.threadptr.restore_thread_pieces(thread_backup_pieces)
            
            self.setConstraints(u - du)
            B[i_pert] = self.getXYZ().flatten()
            self.threadptr.restore_thread_pieces(thread_backup_pieces)
        return A,B
