#include <Eigen/Core>
#include <Eigen/Geometry>
#include <Eigen/Cholesky>
#include <Eigen/LU>
#include <Eigen/SVD>
#include <math.h>
#include <iostream>
#include <fstream>
#include <climits>
#include <vector>
#include <algorithm>

#include "../DiscreteRods/thread_discrete.h"


USING_PART_OF_NAMESPACE_EIGEN
using namespace std;

void writeMatrix(MatrixXd& x,int i);
MatrixXd readMatrix(int i);

void dumpThread(Thread* thread);
void loadConstraints(Thread* thread);

