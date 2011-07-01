import numpy as np
import socket

execfile("consts.m")

class Wormhole:
    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        print "waiting for connection"
        self.conn, addr = s.accept() # hangs until other end connects
        print 'Connection address:', addr
        
    def put(self,name,val):
        val = np.atleast_2d(val)
        self.conn.send(("%"+str(L_CMD)+"s")%"put")
        self.conn.send(("%"+str(L_NAME)+"s")%name)
        self.conn.send(("%"+str(L_SHAPE)+"s")%str(val.shape).replace("(","[").replace(")","]"))
        n_floats = val.size
        n_sent = 0
        val_str = val.astype('>f8').tostring(order='F')
        while n_sent < n_floats:
            n_tosend = min(L_BUFFER/8,n_floats-n_sent)
            self.conn.send(val_str[8*n_sent:8*(n_sent+n_tosend)])
            n_sent += n_tosend
            #print "%i/%i floats sent"%(n_sent,n_floats)
            
    def execute(self,stmt):
        self.conn.send(("%"+str(L_CMD)+"s")%"exec")
        print ("%"+str(L_STMT)+"s")%stmt
        self.conn.send(("%"+str(L_STMT)+"s")%stmt)
        
    def get(self,name):
        self.conn.send(("%"+str(L_CMD)+"s")%"get")
        self.conn.send(("%"+str(L_NAME)+"s")%name)
        shape = tuple(map(int,self.conn.recv(L_SHAPE).split()))
        n_floats = np.prod(shape)
        val_flat = np.zeros(n_floats)        
        n_read = 0
        while n_read < n_floats:
            n_toread = min(L_BUFFER/8,n_floats-n_read)
            val_flat[n_read:n_read+n_toread] = np.fromstring(self.conn.recv(n_toread*8),'>f8')
            n_read += n_toread
            #print "%i/%i floats read"%(n_read,n_floats)
            
        return val_flat.reshape(shape,order="F")
            
            
            
        

        
