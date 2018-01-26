#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <boost/python/class.hpp>
#include <boost/python/numpy.hpp>
#include <stdexcept>

#include "dynamic.h"

namespace p = boost::python;
namespace np = boost::python::numpy;

class Grid
{
public:
  Grid(np::ndarray g)
  : py_grid(g)
  {
    try
    {
        if (g.shape(0) <= 0 || g.shape(1) <= 0)
          throw std::runtime_error("Grid not valid");
        else
          this->grid_matrix = nd_array_to_matrix(g);
    }
    catch (const std::exception & e)
    {
      std::cout << e.what();
    }
  }
  void next_gen(int threshold=5)
  {
    MatrixXd I = dynamic::incase(this->grid_matrix);
    for (int i = 0; i < I.innerSize()-1; i++)
      for (int j = 0; j < I.outerSize()-1; j++)
        if (i != 0 && j != 0)
          (this->grid_matrix)(i-1,j-1) = dynamic::alive_Moore(I,i-1,j-1,threshold);
    this->py_grid = matrix_to_nd_array(this->grid_matrix);
  }
  np::ndarray get_grid()
  {
    return this->py_grid;
  }
  np::ndarray get_next_gen(int threshold=5)
  {
    next_gen(threshold);
    return this->py_grid;
  }
protected:
    MatrixXd nd_array_to_matrix(np::ndarray & py_array)
    {
      MatrixXd M(py_array.shape(0), py_array.shape(1));
      for (int i = 0; i < py_array.shape(0); i++)
        for (int j = 0; j < py_array.shape(0); j++)
          M(i,j) = p::extract<double>(py_array[i][j]);
      return M;
    }
    np::ndarray matrix_to_nd_array(MatrixXd & M)
    {
      p::tuple shape = p::make_tuple(M.innerSize(),M.outerSize());
      np::dtype dtype = np::dtype::get_builtin<int>();
      np::ndarray py_array = np::empty(shape,dtype);
      for (int i = 0; i < M.innerSize(); i++)
        for (int j = 0; j < M.outerSize(); j++)
          py_array[i][j] = M(i,j);
      return py_array;
    }
    np::ndarray py_grid;
    MatrixXd grid_matrix;
};

using namespace boost::python;
BOOST_PYTHON_MODULE(dynamic_ext)
{
  np::initialize();
  class_<Grid>("Grid", init<np::ndarray>())
    .def("next_gen", &Grid::next_gen)
    .def("get_grid",&Grid::get_grid)
    .def("get_next_gen",&Grid::get_next_gen)
  ;

}
