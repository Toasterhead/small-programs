import math, copy
    
class Vector(object):
  """A class for storing vector information and performing vector operation."""
  
  def __init__(self, array):
    """The Vector constructor."""
    
    assert type(array) is list or type(array) is tuple
    assert len(array) > 0
    
    for item in array: assert type(item) in (float, int)
      
    self._vector = tuple(array)
    
  @property
  def Size(self): return len(self._vector)
  
  def get_value(self, index):
    """Returns the value at the specified index."""
    
    assert type(index) is int and index >= 0 and index < self.Size
    
    return self._vector[index]
    
  def get_data(self):
    """Retuns all vector information as a tuple."""
    
    return copy.deepcopy(self._vector)

  def negation(self):
    """Returns the negation of the vector."""

    array = []
    for i in range(self.Size): array.append(-self._vector[i])

    return Vector(array)
    
  def magnitude(self):
    """Returns the magnitude of the vector."""
    
    num = 0
    
    for i in self._vector: num += pow(i, 2)
    
    return math.sqrt(num)
    
  def angle(self): #Under construction.
    """Returns the angle of a vector when the displacements form a
    right triangle."""
    
    assert self.Size == 2 #Temporary limitation to simplify testing.
    
    return math.atan(self._vector[1] / self._vector[0]) #Doesn't account for QII and QIII.

  def angle_between(self, other):
    """Returns the angle between this vector and another in degrees."""

    assert type(other) is Vector

    dotProduct        = self.dot_product(other)
    magnitudeProduct  = self.magnitude() * other.magnitude()

    return math.acos(dotProduct / magnitudeProduct) * (180 / math.pi)

  def perpendicular_to(self, other):
    """Determines whether this vector is perpendicular to another
    and returns the result."""

    assert type(other) is Vector

    return self.dot_product(other) == 0
    
  def normalized(self):
    """Returns a vector with a magnitude of 1."""

    result = []

    for i in range(len(self._vector)):
      result.append(self._vector[i] / self.magnitude())

    return Vector(result)
    
  def add(self, other):
    """Returns the result of adding another vector to this one."""
    
    assert type(other) is Vector
    
    result = []
    
    for i in range(self.Size): 
      result.append(self._vector[i] + other.get_value(i))
    
    return Vector(result)
    
  def subtract(self, other):
    """Returns the result of subracting another vector from this one."""
    
    return self.add(other.inverted())
    
  def multiply(self, scalar):
    """Returns the result of multiplying the vector by a scalar."""
    
    assert type(scalar) is float or type(scalar) is int
    
    result = []
    
    for i in range(self.Size):
      result.append(scalar * self._vector[i])
      
    return Vector(result)

  def divide(self, scalar):
    """Returns the result of dividing the vector by a scalar."""

    return self.multiply(1 / scalar)
    
  def dot_product(self, other):
    """Returns the dot product of multiplying this vector with another."""
    
    assert type(other) is Vector
    
    result = 0
    
    for i in range(self.Size):
      result += self._vector[i] * other.get_value(i)
      
    return result
    
  def cross_product(self, other):
    """Returns the cross product of multiplying this vector with another."""
    
    assert type(other) is Vector and other.Size == 3
    
    return Vector([
      self.get_value(1) * other.get_value(2) - self.get_value(2) * other.get_value(1),
      self.get_value(2) * other.get_value(0) - self.get_value(0) * other.get_value(2),
      self.get_value(0) * other.get_value(1) - self.get_value(1) * other.get_value(0)])

  def __str__(self):
    """Returns a string representation of the vector."""

    s = "["

    if self.Size > 1:
      for i in range(self.Size - 1): s += str(self._vector[i]) + ", "

    s += str(self._vector[self.Size - 1]) + "]"

    return s
