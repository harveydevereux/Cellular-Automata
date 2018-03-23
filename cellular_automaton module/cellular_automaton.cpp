#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <boost/python/class.hpp>
#include <boost/python/numpy.hpp>
#include <stdexcept>
#include <string>
#include <iostream>

#include "cellular_automaton.h"

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
  /*
    butterflies where a mistake! get them with i-1,j-1 passed to alive_conway,
    and also changing JUST the block indexes to i,j in alive_conway.
  */
  void next_gen(int threshold)
  {
    MatrixXd I = cellular_automaton::incase(this->grid_matrix);
    for (int i = 0; i < I.innerSize()-1; i++)
      for (int j = 0; j < I.outerSize()-1; j++)
        if (i != 0 && j != 0){
          if (this->criterion == "Moore")
            (this->grid_matrix)(i-1,j-1) = cellular_automaton::alive_Moore(I,i-1,j-1,threshold);
          if (this->criterion == "Conway")
            (this->grid_matrix)(i-1,j-1) = cellular_automaton::alive_conway(I,i,j);
        }
    this->py_grid = matrix_to_nd_array(this->grid_matrix);
  }
  np::ndarray get_grid()
  {
    return this->py_grid;
  }
  np::ndarray get_next_gen(int threshold)
  {
    next_gen(threshold);
    return this->py_grid;
  }
   void set_grid(np::ndarray & py_arr)
  {
    this->py_grid = py_arr;
    this->grid_matrix = nd_array_to_matrix(py_arr);
  }
  void set_model(std::string name)
  {
    this->criterion = name;
  }
protected:
    MatrixXd nd_array_to_matrix(np::ndarray & py_array)
    {
      MatrixXd M(py_array.shape(0), py_array.shape(1));
      for (int i = 0; i < py_array.shape(0); i++)
        for (int j = 0; j < py_array.shape(0); j++)
          M(i,j) = p::extract<int>(py_array[i][j]);
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
    std::string criterion = "Moore";
};

using namespace boost::python;
BOOST_PYTHON_MODULE(cellular_automaton)
{
  np::initialize();
  class_<Grid>("Grid", init<np::ndarray>())
    .def("next_gen", &Grid::next_gen)
    .def("get_grid",&Grid::get_grid)
    .def("get_next_gen",&Grid::get_next_gen)
    .def("set_grid",&Grid::set_grid)
    .def("set_model",&Grid::set_model)
  ;

}
