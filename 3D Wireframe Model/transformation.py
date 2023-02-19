import math, matrix

def translate(dx, dy, dz = None):
  """Returns a transformation matrix for translation."""
  
  assert type(dx) in (float, int)
  assert type(dy) in (float, int)
  assert type(dz) in (float, int) or dz == None
  
  if dz == None:
    return matrix.Matrix([[1, 0, dx], [0, 1, dy], [0, 0, 1]])
  
  return matrix.Matrix([[1, 0, 0, dx], [0, 1, 0, dy], [0, 0, 1, dz], [0, 0, 0, 1]])

def scale(sx, sy, sz = None): 
  """Returns a transformation matrix for scaling."""
  
  assert type(sx) in (float, int)
  assert type(sy) in (float, int)
  assert type(sz) in (float, int) or sz == None
  
  if sz == None:
    return matrix.Matrix([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
  
  return matrix.Matrix([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]])
  
def rotate(theta):
  """Returns a transformation matrix for two-dimensional rotation."""
  
  assert type(theta) in (float, int)
  
  DEG_TO_RAD = math.pi / 180
  
  return matrix.Matrix([
    [math.cos(theta * DEG_TO_RAD),  -math.sin(theta * DEG_TO_RAD),  0],
    [math.sin(theta * DEG_TO_RAD),  math.cos( theta * DEG_TO_RAD),  0],
    [0,                             0,                              1]])
  
def roll(theta): 
  """Returns a transformation matrix for rotation about the Z-axis.
  For use with 3D position matrices only."""
  
  assert type(theta) in (float, int)
  
  DEG_TO_RAD = math.pi / 180
  
  return matrix.Matrix([
    [math.cos(theta * DEG_TO_RAD),  -math.sin( theta * DEG_TO_RAD), 0, 0],
    [math.sin(theta * DEG_TO_RAD),  math.cos(  theta * DEG_TO_RAD), 0, 0],
    [0,                             0,                              1, 0],
    [0,                             0,                              0, 1]])
    
def pitch(theta): 
  """Returns a transformation matrix for rotation about the X-axis.
  For use with 3D position matrices only."""
  
  assert type(theta) in (float, int)
  
  DEG_TO_RAD = math.pi / 180
  
  return matrix.Matrix([
    [1,                             0, 0,                               0],
    [0, math.cos(theta * DEG_TO_RAD),  -math.sin( theta * DEG_TO_RAD),  0],
    [0, math.sin(theta * DEG_TO_RAD),  math.cos(  theta * DEG_TO_RAD),  0],
    [0,                             0, 0,                               1]])
    
def yaw(theta):
  """Returns a transformation matrix for rotation about the Y-axis.
  For use with 3D position matrices only."""
  
  assert type(theta) in (float, int)
  
  DEG_TO_RAD = math.pi / 180
  
  return matrix.Matrix([
    [math.cos(theta * DEG_TO_RAD),  0, math.sin(theta * DEG_TO_RAD),  0], 
    [0,                             1, 0,                             0],
    [-math.sin(theta * DEG_TO_RAD), 0, math.cos(theta * DEG_TO_RAD),  0],
    [0,                             0, 0,                             1]])
    
def about_anchor(transMatrix, x, y, z = None):
  """Processes the given tranformation matrix about an anchor point."""

  is2D = (transMatrix.Width == 3 and transMatrix.Height == 3)
  is3D = (transMatrix.Width == 4 and transMatrix.Height == 4)
  
  assert type(transMatrix)  is matrix.Matrix
  assert type(x)            in (int, float)
  assert type(y)            in (int, float)
  assert type(z)            in (float, int) or z == None
  assert is2D or is3D
  
  fromOrigin  = None
  toOrigin    = None
  
  if z == None:
    fromOrigin  = translate(x, y)
    toOrigin    = translate(-x, -y)
  else:
    fromOrigin  = translate(x, x, z)
    toOrigin    = translate(-x, -y, -z)
  
  return fromOrigin.multiply(transMatrix).multiply(toOrigin)
  
def position_matrix(x, y, z = None):
  """Returns the given coordinates as a position matrix."""
  
  assert type(x) in (float, int)
  assert type(y) in (float, int)
  assert type(z) in (float, int) or z == None
  
  if z == None:
    return matrix.Matrix([[x,],[y,],[1,]])
  
  return matrix.Matrix([[x,],[y,],[z,],[1,]])
