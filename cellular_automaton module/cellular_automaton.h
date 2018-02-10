#include <iostream>
#include <Eigen/Dense>
using Eigen::MatrixXd;

namespace cellular_automaton{

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

bool alive_Moore(const MatrixXd & M, int i, int j, int threshold)
{
  int count = 0;
  count = ((M.block(i,j,3,3)).sum()-(M.block(i,j,3,3))(1,1));
  return (count>=threshold);
}

/*
void simulate(MatrixXd & M, int threshold)
{
  MatrixXd I = incase(M);
  int Row = I.innerSize();
  int Col = I.outerSize();
  for (int i = 0; i < I.innerSize()-1; i++)
    for (int j = 0; j < I.outerSize()-1; j++)
      if (i != 0 && j != 0)
        M(i-1,j-1) = alive_Moore(I,i-1,j-1,threshold);
}
*/

}
