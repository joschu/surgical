#ifndef _threadutils_discrete_h
#define _threadutils_discrete_h

#include <Eigen/Core>
#include <Eigen/Geometry>
#include <math.h>
#include <iostream>
#include <fstream>
#include <climits>
#include <vector>
#include <algorithm>


// import most common Eigen types
USING_PART_OF_NAMESPACE_EIGEN
using namespace std;


typedef Matrix<double, 2, 3> Matrix23d;

double Normal(double mu, double sigma);
void rotate_between_tangents(const Vector3d& start_tan, const Vector3d& end_tan, Matrix3d& rotation);
void make_vectors_perpendicular(const Vector3d& start, Vector3d& to_be_perp); //also normalizes
double angle_mismatch(const Matrix3d& Q, const Matrix3d& R);
double angle_diff(const double goal_angle, const double start_angle);
bool compare_vector_norms(Vector3d& first, Vector3d& second);
void skew_symmetric_for_cross(const Vector3d& vec, Matrix3d& skew_mat);
void skew_symmetric_for_cross_fast(const Vector3d& vec, Matrix3d& skew_mat);
double calculate_magnitude_squared(vector<Vector3d>& to_mag); 
double calculate_vector_diff_norm(vector<Vector3d>& pts1, vector<Vector3d>& pts2);
double calculate_vector_norm_avg(vector<Vector3d>& pts1, vector<Vector3d>& pts2);
double distance_between_points(Vector3d point1, Vector3d point2);
double angle_between(const Vector3d& tan1, const Vector3d& tan2);
void rotation_from_euler_angles(Matrix3d& rotation, double angZ, double angY, double angX);

void writeParams(std::string file, double* towrite);
void readParams(std::string file, double* out);

struct Frame_Motion
{
	Vector3d _pos_movement;
	Matrix3d _frame_rotation;

	Frame_Motion(){};

  Frame_Motion(const Frame_Motion& toCopy) :
    _pos_movement(toCopy._pos_movement), _frame_rotation(toCopy._frame_rotation){};

  Frame_Motion(const Vector3d& pos_movement, const Matrix3d& frame_rotation);
  Frame_Motion(const Vector3d& pos_movement, const Vector3d& rotation_axis, const double rotation_ang);
  void set_movement(const Vector3d& pos_movement){_pos_movement = pos_movement;};
  void set_rotation(const Matrix3d& frame_rotation){_frame_rotation = frame_rotation;};
	void applyMotion(Vector3d& pos, Matrix3d& frame);
	Frame_Motion& operator=(const Frame_Motion& rhs);

};




#endif

