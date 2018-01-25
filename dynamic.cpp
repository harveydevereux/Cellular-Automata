#include <iostream>
#include <Eigen/Dense>

using Eigen::MatrixXd;

MatrixXd incase(const MatrixXd & A)
{
  int Row_a = A.innerSize();
  int Col_a = A.outerSize();
  int Row_b = Row_a+2;
  int Col_b = Col_a+2;
  MatrixXd B(Row_b,Col_b);
  B.setZero();
  B.block(1,1,Row_a,Col_a) = A;
  for (int i = 0; i < Row_b-2; i++)
  {
    B(i+1,0) = (A.col(Col_a-1))(i);
    B(i+1,Col_b-1) = (A.col(0))(i);
  }
  for (int j = 0; j < Col_b-2; j++)
  {
    B(0,j+1) = (A.row(Row_a-1))(j);
    B(Row_b-1,j+1) = (A.row(0))(j);
  }
  B.topLeftCorner(1,1) = A.bottomRightCorner(1,1);
  B.topRightCorner(1,1) = A.bottomLeftCorner(1,1);
  B.bottomLeftCorner(1,1) = A.topRightCorner(1,1);
  B.bottomRightCorner(1,1) = A.topLeftCorner(1,1);
  return B;
}

bool alive_Moore(const MatrixXd & M, int threshold=5)
{
  int count = 0;
  // to complete
  return 0;
}

void simulate(MatrixXd & M)
{
  M = incase(M);
  int Row = M.innerSize();
  int Col = M.outerSize();

  for (int i = 0; i < M.innerSize()-1; i++)
    for (int j = 0; j < M.outerSize()-1; j++)
      if (i != 0 && j != 0)
        // do stuff
        continue;
}

int main(int argc, char ** argv)
{
  int r = 4;
  int c = 4;
  MatrixXd m(r,c);
  m << 1, 0, 1, 0,
       0, 1, 1, 1,
       1, 1, 0, 0,
       0, 1, 1, 0;
  //std::cout << m << std::endl;
  MatrixXd b(r+2,c+2);
  b = incase(m);
  std::cout << b << std::endl;
  MatrixXd C(r,c);
  for (int i = 0; i < b.innerSize()-1; i++)
    for (int j = 0; j < b.outerSize()-1; j++)
      if (i != 0 && j != 0)
        C(i-1,j-1) = b(i,j);
  std::cout << C;
  return 0;
}
