import copy

class Matrix(object):
  """A class for storing matrix data and performing matrix operations."""
  
  def __init__(self, array):
    """The Matrix constructor."""
    
    assert type(array) in (list, tuple) and len(array) > 0
    
    for item in array:
      assert type(item) in (list, tuple)
      assert len(item) > 0
      assert len(item) == len(array[0])
      
    self._matrix = copy.deepcopy(array)
    
  @property
  def Width(self):  return len(self._matrix[0])
  @property
  def Height(self): return len(self._matrix)
  
  def get_value(self, column, row):
    """Returns the value stored at the specified location."""
    
    assert type(column) is int and column >= 0 and column < self.Width
    assert type(row)    is int and row    >= 0 and row    < self.Height
    
    return self._matrix[row][column]
    
  def get_data(self):
    """Returns the entire matrix as a multi-dimensional list."""
    
    return copy.deepcopy(self._matrix)

  def equals(self, other):
    """Determines if this matrix is equal to another and returns
    the result."""

    assert type(other) is Matrix

    for rowIndex in range(len(self._matrix)):
      for value in range(len(self._matrix[rowIndex])):
        if self._matrix[rowIndex][value] != other.get_value(value, rowIndex):

          return False

    return True
    
  def transposed(self):
    """Returns the transposition of the matrix."""

    result = []

    for i in range(self.Width):
      vector = []
      for j in range(self.Height):
        vector.append(self._matrix[j][i])
      result.append(vector)

    return Matrix(result)
    
  def add(self, other):
    """Returns the result of adding this matrix to another."""
    
    assert type(other) is Matrix
    
    result = []
    
    for i in range(self.Height):
      vector = []
      for j in range(self.Width):
        vector.append(self._matrix[j][i] + other.get_value(j, i))
      result.append(vector)
      
    return Matrix(result)
    
  def subtract(self, other):
    """Returns the result of subtracting another matrix from this one."""
    
    return self.add(other.inverted())

  def multiply(self, other):
    """Returns the result of mulitplying this matrix with another."""

    assert type(other) is Matrix

    result = []

    for i in range(self.Height):
      vector = []
      for j in range(other.Width):
        vector.append(
          Matrix._dot_product(
            Matrix._extract_vector(self,   i, False),
            Matrix._extract_vector(other,  j, True)))
      result.append(vector)

    return Matrix(result)
    
  def multiply_by_scalar(self, scalar):
    """Returns the result of multiplying this matrix by a scalar."""
    
    assert type(scalar) is float or type(scalar) is int
    
    result = []
    
    for i in range(self.Height):
      vector = []
      for j in range(self.Width):
        vector.append(self._matrix[j][i] * scalar)
      result.append(vector)
      
    return Matrix(result)

  def divide_by_scalar(self, scalar):
    """Returns the result of dividing this matrix by a scalar."""
    
    return self.multiply(1 / scalar)

  def _extract_vector(matrix, index, byColumn = False):
    """Returns a list representing a vector extracted from the given
    horizontal or vertical index. For internal use only."""

    assert type(matrix)   is Matrix
    assert type(index)    is int and index >= 0
    assert type(byColumn) is bool
    assert index < matrix.Height if byColumn == False else index < matrix.Width

    matrixData  = matrix.get_data()
    result      = []

    if byColumn == False:
      for i in matrixData[index]: result.append(i)
    else:
      for i in range(matrix.Height):  result.append(matrixData[i][index])

    return result

  def _dot_product(left, right):
    """Receives two lists representing vectors and returns their dot
    product. For internal use only."""

    assert type(left)   is list
    assert type(right)  is list
    assert len(left) == len(right)

    result = 0
    
    for i in range(len(left)):
      result += left[i] * right[i]
      
    return result

  def __str__(self):
    """Returns a string representation of the matrix."""

    return " " #Finish later.
