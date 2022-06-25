"""
This module is used for functions and classes that may be useful in another projects
related to math, physics, etc. Basically school in general.
"""

class VectorError(Exception):
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
    def __init__(self, *args):
        if len(args) < 2: 
            if not isinstance(args, (list, tuple)): raise VectorError("Not enough values")
            else: self.args = list(args[0])
        else: self.args = list(args)
        self.magnitude = sum(map(lambda x: x*x, self.args))
    
    def eval(self, result, other, valid) -> bool:
        """
        eval takes a result, an object and the type of objects it
        can receive, it checks if the type of the object is in
        the accepted objects and returns the result if so, else
        raises an error.
        """
        if isinstance(other, valid): return result
        raise VectorError("Invalidad operation")
    
    def __getitem__(self, index):
        """
        returns index-nth component of the vector.
        """
        if index < len(self) and index >= -len(self): return self.args[index]
        raise VectorError("Component out of range")
    
    def __setitem__(self, index, value):
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

if __name__ == '__main__':
    a = Vector([1, 2, 3])
    b = Vector([1, 2, 3, 4])
    print(-b)
