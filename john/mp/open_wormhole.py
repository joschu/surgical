import numpy as np
import socket
from time import sleep
execfile("consts.m")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((PYTHON_IP, TCP_PORT))
s.listen(1)

print "waiting for connection"
conn, addr = s.accept() # hangs until other end connects
print 'Connection address:', addr

while True:
    print "waiting for message"
    cmd_class = conn.recv(L_CMD).strip()
    print "cmd_class: ",cmd_class
    if cmd_class == 'put':
        name = conn.recv(L_NAME).strip()
        print "name: ",name
        shape_str = conn.recv(L_SHAPE).strip()
        print "shape_str: ",shape_str
        shape = tuple(map(int,shape_str.split()))
        n_floats = np.prod(shape)
        targ_flat = np.zeros(n_floats,'float')        
        n_read = 0
        while n_read < n_floats:
            n_toread = min(L_BUFFER/8,n_floats-n_read)
            arr = np.fromstring(conn.recv(n_toread*8),dtype='>f8')
            targ_flat[n_read:n_read+n_toread] = arr
            n_read += n_toread
            #print "%i/%i floats read"%(n_read,n_floats)           
        targ = targ_flat.reshape(shape,order="F")
        print "received array: ",targ
        exec("%s = targ"%name)
    elif cmd_class == 'exec':
        stmt = conn.recv(100).strip()
        print "statment: ",stmt
        exec(stmt)
    elif cmd_class == "get":
        name = conn.recv(10).strip()
        print "getting variable: ",name
        try:
            exec("src = %s"%name)
        except NameError:
            exec("src = []")
        src = np.atleast_2d(src)
        conn.send("%30s"%str(src.shape).replace(")","]").replace("(","["))
        src_str = src.astype('>f8').tostring(order="F")
        n_floats = src.size
        n_sent = 0
        while n_sent < n_floats:
            n_tosend = min(L_BUFFER,n_floats-n_sent)            
            conn.send(src_str[n_sent*8:(n_sent+n_tosend)*8])
            n_sent += n_tosend
            #print "%i/%i floats sent"%(n_sent,n_tosend)  
    else:
        raise Exception("unrecognized command")
        
            
        
    