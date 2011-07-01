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

MatrixXd readMatrix(int i) {
  MatrixXd m;
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
  //std::cout << "reading matrix " << R << "x" << C << std::endl;
  for (int r=0; r<R; r++) {
    for (int c=0; c<C; c++) {
      in >> value;
      //std::cout << value << " ";
      m(r,c) = value;
    }
    //std::cout << std::endl;
  }
  in.close();
  //std::cout << "done reading" << std::endl;
  return m;
}

void loadThread(Thread* thread) {
  // x1 y1 z1 x2 y2 z2 ...
  VectorXd m = readMatrix(0).transpose();
  thread->copy_data_from_vector(m);  
}

MatrixXd threeToX(Matrix3d& x) {
  MatrixXd m1;  
  m1 = MatrixXd::Identity(3,3);
  for (int r=0; r < 3; r++)
    for (int c=0; c < 3; c++)
      m1(r,c) = x(r,c);
  return m1;
}

Vector3d XTo3(MatrixXd& x) {
  Vector3d v;
  //std::cout << x.rows() << " " << x.cols() << std::endl;
  for (int c=0; c<3; c++) {
    v(c) = x(0,c);
  }
}

void dumpThread(Thread* thread) {
  
  // vertices  
  MatrixXd m;  
  //std::cout << "dumping verts" << std::endl; 
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
  
  //std::cout << "dumping start rot" << std::endl;   
  // start rot
  Matrix3d start_rot = thread->start_rot();
  MatrixXd start_rotX = threeToX(start_rot);
  writeMatrix(start_rotX,1);

  Matrix3d end_rot = thread->end_rot();
  MatrixXd end_rotX = threeToX(end_rot);
  writeMatrix(end_rotX,2);

}

void loadConstraints(Thread* thread) {
    Vector3d start_pos = readMatrix(0).transpose();
    //std::cout << "start:" << start_pos(0) << " " << start_pos(1) << " " << start_pos(2) << std::endl;
    Matrix3d start_rot = readMatrix(1);
    Vector3d end_pos = readMatrix(2).transpose();
    //std::cout << "end:" << end_pos(0) << " " << end_pos(1) << " " << end_pos(2) << std::endl;
    Matrix3d end_rot = readMatrix(3);
    thread->set_constraints(start_pos,start_rot,end_pos,end_rot);
}


//MatrixXd makePerts(Thread* thread, double eps)
//{
  //int n_seg = thread->num_pieces();
  //int n_ctl = 12;
  
  //MatrixXd A = MatrixXd(n_seg,n_ctl);
  //MatrixXd B = MatrixXd(n_seg,n_ctl);
  
  //vector<ThreadPiece*> thread_backup_pieces;
  //thread->save_thread_pieces_and_resize(thread_backup_pieces);

  //VectorXd du(n_ctl);
  
  //for(int i_ctl = 0; i_ctl < n_ctl; i_ctl++)
  //{
    //du.setZero();   
    
    //du(i_ctl) = eps;        
    ////applyControl(thread, du);
    //for (int i_seg=0; i_seg < n_seg; i_seg++)
    //{
      //A.block(i_seg*3, i_ctl, 3,1) = thread->vertex_at_ind(i_seg);
    //}
    //thread->restore_thread_pieces(thread_backup_pieces);

    //du(i_ctl) = -eps;
    ////applyControl(thread, du);
    //for (int i_seg=0; i_seg < n_seg; i_seg++)
    //{
      //B.block(3*n_seg, i_ctl, 3,1) = thread->vertex_at_ind(i_seg);
    //}
    //thread->restore_thread_pieces(thread_backup_pieces);

  //}
//}

//void applyControl(Thread* thread, VectorXd du) {
  //u = 
//}