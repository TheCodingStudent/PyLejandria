"""
This module is used for functions and classes that may be useful in another projects
related to math, physics, etc. Basically school in general.
"""

import math
from pylejandria.tools import prettify
from typing import Any, ClassVar, List, Optional, Tuple

class VectorError(Exception):
    """
    Custom Exception for Vector class.
    """
    pass

class MatrixError(Exception):
    """
    Custom Exception for Vector class.
    """
    pass

class Vector:
    """
    The class Vector is always necessary for videogames or school, its basic funcionality
    is give all the components of the vector and be able to use all its operators, vector
    addition, subtraction, scalar multiplication, cross and dot product.
    """
    def __init__(self, *args: List[int|float]) -> None:
        if len(args) < 2: 
            if not isinstance(args, (list, tuple)): raise VectorError("Not enough values")
            else: self.args = list(args[0])
        else: self.args = list(args)
        self.magnitude = sum(map(lambda x: x*x, self.args))
    
    def eval(self, result: Any, other: Any, valid: Tuple[Any]) -> bool:
        """
        eval takes a result, an object and the type of objects it
        can receive, it checks if the type of the object is in
        the accepted objects and returns the result if so, else
        raises an error.
        """
        if isinstance(other, valid): return result
        raise VectorError("Invalidad operation")
    
    def __getitem__(self, index: Tuple[int, int]) -> int|float:
        """
        returns index-nth component of the vector.
        """
        if index < len(self) and index >= -len(self): return self.args[index]
        raise VectorError("Component out of range")
    
    def __setitem__(self, index: Tuple[int, int], value: int|float) -> None:
        """
        sets the index-nth component of the vector to the given value
        """
        if index < len(self) and index >= -len(self): self.args[index] = value
        else: raise VectorError("Component out of range")
    
    def __add__(self, other):
        """
        returns the sum of this vector and another vector.
        """
        if isinstance(other, (Vector, )):
            a, b = self.args, other.args
            if len(self) < len(other): a += [0] * (len(other) - len(self))
            else: b += [0] * (len(self) - len(other))
            return Vector(map(lambda x, y: x+y, a, b))

    __sub__ = lambda self, other: self + (-other)                                                               # subtracts vector B to vector A
    __neg__ = lambda self: self * -1                                                                            # inverts the vector multiplying by -1
    __len__ = lambda self: len(self.args)                                                                       # returns the number of components of the vector
    __mul__ = lambda self, other: self.eval(Vector(map(lambda x: other*x, self.args)), other, (int, float))     # multiply by scalar
    __rmul__ = lambda self, other: self * other                                                                 
    __gt__ = lambda self, other: self.eval(self.magnitude > other.magnitude, other, (Vector, ))                 # returns if vector A is greater than vector B
    __lt__ = lambda self, other: self.eval(self.magnitude < other.magnitude, other, (Vector, ))                 # returns if vector A is less than vector B
    __ge__ = lambda self, other: self.eval(self.magnitude >= other.magnitude, other, (Vector, ))                # returns if vector A is greater or equal than vector B
    __le__ = lambda self, other: self.eval(self.magnitude <= other.magnitude, other, (Vector, ))                # returns if vector A is less or equal than vector B
    __ne__ = lambda self, other: self.eval(self.args != other.args, other, (Vector, ))                          # returns if vector A is not equal to vector B
    __eq__ = lambda self, other: self.eval(self.args == other.args, other, (Vector, ))                          # representation of the vector for print in console
    __repr__ = lambda self: str(self.args)

class Matrix:
    def __init__(self, matrix:List[List[int|float]], dim: Tuple[int, int]=()) -> None:
        """
        Matrix is a representation of algebra matrix, is takes a list of lists
        of numbers. It contains functions matrix addition, subtraction, multiplication,
        scalar multiplication, get determinant and many things we plan to add.
        """
        if matrix != None:                                                                          # if there is matrix then we dont check for dimension
            if any([len(row) != len(matrix[0]) for row in matrix]):                                 # all rows should be the same length
                raise MatrixError('Invalid Matrix dimension')                                       # if not then we raise an error
            self.matrix = matrix                                                                    # we set the dimension
        else: 
            if len(dim) != 2: raise MatrixError("Invalid Matrix dimension")                         # if dim is not a tuple with 2 values we raise an dim error
            if dim[0] < 1 or dim[1] < 1: raise MatrixError("Dimension must be greater than 0")      # dimensions must be greater than 1
            if dim[0] == 1 and dim[1] == 1: raise MatrixError("Matrix cannot be 1x1")               # both dimensions cannot be 1
            self.matrix = [[1 for _ in range(dim[0])] for _ in range(dim[1])]                       # we make a matrix full of one's
        self.rows, self.cols = len(self.matrix), len(self.matrix[0])                                # we set columns and row
        self.is_square = len(self.matrix) == len(self.matrix[0])                                    # we check if matrix is square
        self.dim = (self.cols, self.rows)                                                           # we save the dimension
        self.determinant = self.get_determinant(self.matrix) if self.is_square else None            # we calculate determinant if matrix is square
    
    def get_determinant(self, matrix:List[List]) -> float:
        """
        this function is made to get determinant of the given matrix, it can be used
        externally but it wasnt intended at first. The determinant is calculated using
        recursion, if the dimension is 2 then we return ad-bc.
        """
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    def valid_value(self, index:Tuple[int, int]) -> bool:
        """
        generic function of Matrix to check if the given pair of coordinates is
        in the range of the matrix.
        """
        x, y = index
        return all([
            x < self.cols,
            x >= -self.cols,
            y < self.rows,
            y >= -self.rows
        ])
    
    def return_value(self, index:Tuple[int, int]) -> float:
        """
        checks if the given index is valid and if so returns the
        corresponding value, if not raise an error.
        """
        x, y = index
        if not self.valid_value(index): raise MatrixError("Invalid Matrix index")
        return self.matrix[y][x]
    
    def row(self, index:int) -> list:
        """
        returns index-nth row of the matrix.
        Example:
            a = Matrix(
                [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ]
            )
            a.row(2) -> [7, 8, 9]
        """
        if index < self.rows and index >= -self.rows: return self.matrix[index]
        raise MatrixError("Invalid row index")
    
    def col(self, index:int) -> list:
        """
        returns index-nth column of the matrix.
        Example:
            a = Matrix(
                [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ]
            )
            a.col(1) -> [2, 5, 8]
        """
        if index < self.cols and index >= -self.cols: return [row[index] for row in self.matrix]
        raise MatrixError("Invalid column index")
    
    def __getitem__(self, indices:Tuple[int, int]|Tuple[Tuple[int, int]]) -> float|List[int|float]:
        """
        if index is a single pair of numbers then it returns the corresponding
        value of the matrix, but if multiple indices in form of tuples are 
        given inside the [] then returns a list of the corresponding values for each index.
        Example:
            a = Matrix(
                [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ]
            )
            a[2, 1] -> 6
            a[(0, 0), (1, 1), (2, 2)] -> [1, 5, 9]
        """
        if not isinstance(indices[0], tuple): return self.return_value(indices)
        return [self.return_value((x, y)) for x, y in indices]
    
    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.dim != other.dim: raise MatrixError("Matrices must be same order")
            return Matrix(
                [[self[x, y] + other[x, y] for x in range(self.cols)]
                for y in range(self.rows)]
            )
        raise MatrixError("Invalid Matrix addition")
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Matrix(
                [[other*self[x, y] for x in range(self.cols)]
                for y in range(self.rows)]
            )
        elif isinstance(other, Matrix):
            if self.cols != other.rows:
                raise MatrixError("Invalid Matrices dimensions")
            c = Matrix(None, (other.cols, self.rows))
            for i in range(self.rows):
                for j in range(other.cols):
                    c[j, i] = sum(map(lambda x, y: x*y, self.row(i), other.col(j))) 
            return c
        raise MatrixError("Invalid Matrix multiplication")
    
    __repr__ = lambda self: prettify(self.matrix, separator=' ')    # representation of the matrix
    __rmul__ = lambda self, other: self * other                     # reciprocal multiplication
    __neg__ = lambda self: self * -1                                # additive inverse matrix
    __sub__ = lambda self, other: self + (-other)                   # matrix subtraction

DEGREES = False

def set_degrees(value:bool = False) -> None:
    """
    set_degrees receives a boolean as input to globally change
    the angle functions, normally in programming angles are used in
    radians, but for quick calculations of for not used to people
    it can be useful to use degrees.
    """
    global DEGREES
    DEGREES = value

sin = lambda x: math.sin(x if not DEGREES else math.radians(x))
cos = lambda x: math.cos(x if not DEGREES else math.radians(x))
tan = lambda x: math.tan(x if not DEGREES else math.radians(x))

acos = lambda x: math.acos(x) if not DEGREES else math.degrees(math.acos(x))
asin = lambda x: math.asin(x) if not DEGREES else math.degrees(math.asin(x))
atan = lambda x: math.atan(x) if not DEGREES else math.degrees(math.atan(x))
atan2 = lambda y, x: math.atan2(y, x) if not DEGREES else math.degrees(math.atan2(y, x))

if __name__ == '__main__':
    a = Matrix(
        [
            [1, 2, 1, 1],
            [0, 1, 1, 1],
            [2, 3, 1, 1]
        ]
    )
    b = Matrix(
        [
            [2, 5],
            [6, 7],
            [1, 1],
            [1, 1]
        ]
    )
    print(b * a)