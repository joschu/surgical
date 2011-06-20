#include "communication.h"
  

// import most common Eigen types
USING_PART_OF_NAMESPACE_EIGEN
using namespace std;


string itoa(int i) {
   std::string s;
   std::stringstream out;
   out << i;
   s = out.str();
   return s;
}

void writeMatrix(MatrixXd& x, int i) {
  std::ofstream out;
  string fname = "/tmp/matrix"+itoa(i);
  out.open(fname.c_str());
  out << x.rows() << " " << x.cols() << std::endl;
  for (int r=0; r<x.rows(); r++) {
    for (int c=0; c<x.cols(); c++) {
      out << x(r,c) << " ";
    }
    out << std::endl;
  }
  out.close();
}

MatrixXd m;
MatrixXd& readMatrix(int i) {
  std::ifstream in;
  string line;
  int R;
  int C;
  string fname="/tmp/matrix"+itoa(i);
  in.open(fname.c_str());
  in >> R;
  in >> C;
  m.resize(R,C);
  float value;
  std::cout << "reading matrix " << R << "x" << C << std::endl;
  for (int r=0; r<R; r++) {
    for (int c=0; c<C; c++) {
      in >> value;
      std::cout << value << " ";
      m(r,c) = value;
    }
    std::cout << std::endl;
  }
  in.close();
  std::cout << "done reading" << std::endl;
  return m;
}

MatrixXd threeToX(Matrix3d& x) {
  MatrixXd m1;  
  m1 = MatrixXd::Identity(3,3);
  for (int r=0; r < 3; r++)
    for (int c=0; c < 3; c++)
      m1(r,c) = x(r,c);
  return m1;
}

void dumpThread(Thread* thread) {
  
  // vertices  
  
  std::cout << "dumping verts" << std::endl; 
  int R = 3;
  int C = thread->_thread_pieces.size();
  Vector3d v;
  m.resize(R,C);  
  for (int c=0; c < C; c++) {
    v = thread->_thread_pieces[c]->vertex();
    for (int r=0; r < R; r++) {
      m(r,c) = v(r);    
    }
  }
  writeMatrix(m,0);
  
  std::cout << "dumping start rot" << std::endl;   
  // start rot
  Matrix3d start_rot = thread->start_rot();
  MatrixXd start_rotX = threeToX(start_rot);
  writeMatrix(start_rotX,1);

  Matrix3d end_rot = thread->start_rot();
  MatrixXd end_rotX = threeToX(start_rot);
  writeMatrix(end_rotX,2);

}


