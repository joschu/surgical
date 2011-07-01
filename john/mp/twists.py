from nibabel.eulerangles import euler2mat,angle_axis2euler,mat2euler
import numpy as np

def twist_around_axis(thread,angle1,angle2,axis):
    xyz = thread.getXYZ()
    cons = thread.getConstraints()    
    mat1 = euler2mat(*cons[3:6])
    mat2 = euler2mat(*cons[9:12])
    tmat1 = euler2mat(*angle_axis2euler(angle1,axis))
    tmat2 = euler2mat(*angle_axis2euler(angle2,axis))    
    newmat1 = np.dot(tmat1,mat1)
    newmat2 = np.dot(tmat2,mat2)
    neweul1 = mat2euler(newmat1)
    neweul2 = mat2euler(newmat2)

    cons[3:6] = neweul1
    cons[9:12] = neweul2
    thread.setConstraints(cons)
    
def twist_ctrl(thread,angle1,angle2):
    xyz = thread.getXYZ()
    axis1 = xyz[:,1] - xyz[:,0]
    axis2 = xyz[:,-1] - xyz[:,-2]
    cons = thread.getConstraints()
    mat1 = euler2mat(*cons[3:6])
    mat2 = euler2mat(*cons[9:12])
    tmat1 = euler2mat(*angle_axis2euler(angle1,axis1))
    tmat2 = euler2mat(*angle_axis2euler(angle2,axis2))
    newmat1 = np.dot(tmat1,mat1)
    newmat2 = np.dot(tmat2,mat2)
    neweul1 = mat2euler(newmat1)
    neweul2 = mat2euler(newmat2)

    
    #print "orig",cons[blah]
    cons[3:6] = neweul1
    cons[9:12] = neweul2
    thread.setConstraints(cons)
    #print thread.getXYZ()[0]    
    
    #print "set2",cons[blah]
    #print "get2",thread.getConstraints()[blah]

    #print thread.getXYZ()[0]

    