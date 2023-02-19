class Point2D(object):
  """A class for storing and manipulating a two-dimensional point."""
  
  def __init__(self, x, y):
    """The Point2D constructor."""
    
    assert type(x) in (int, float)
    assert type(y) in (int, float)
    
    self._x = x
    self._y = y
    
  @property
  def X(self): return self._x
  @property
  def Y(self): return self._y

  def get_data(self):
    """Returns the point's coordinates as a tuple."""

    return (self._x, self._y)

  def __str__(self):
    """Returns a string representation of the point."""

    return "(" + str(self._x) + ", " + str(self._y) + ")"
    
class Point3D(object):
  """A class for storing and manipulating a three-dimensional point."""
  
  def __init__(self, x, y, z):
    """The Point3D constructor."""
    
    assert type(x) in (int, float)
    assert type(y) in (int, float)
    assert type(z) in (int, float)
    
    self._x = x
    self._y = y
    self._z = z
    
  @property
  def X(self): return self._x
  @property
  def Y(self): return self._y
  @property
  def Z(self): return self._z

  def get_data(self):
    """Returns the point's coordinates as a tuple."""

    return (self._x, self._y, self._z)  
    
  def __str__(self):
    """Returns a string representation of the point."""

    return "(" + str(self._x) + ", " + str(self._y) + ", " + str(self._z) + ")"
