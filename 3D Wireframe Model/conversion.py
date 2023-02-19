import point, vector, matrix, graph

def point_to_vector(thePoint):
    """Converts a point to a vector and returns the result."""

    assert type(thePoint) in (point.Point2D, point.Point3D)
    
    return vector.Vector(thePoint.get_data())

def point_to_vertex(thePoint):
    """Converts the point to a vertex (for use in a graph) and
    returns the result."""
    
    assert type(thePoint) in (point.Point2D, point.Point3D)

    return graph.Vertex(thePoint)

def vector_to_matrix(theVector, horizontal = False):
    """Converts the vector to a single-column or single-row
    matrix and returns the result."""

    assert type(theVector)  is vector.Vector
    assert type(horizontal) is bool
    
    if horizontal == True:
      data = []
      for i in theVector.get_data():
        data.append([i,])
      
      return matrix.Matrix(data)
    
    return matrix.Matrix([theVector.get_data(),])

def vector_from_matrix(theMatrix, index, byColumn = False):
    """Returns a vector extracted from the given horizontal or
    vertical index."""

    assert type(theMatrix)  is matrix.Matrix
    assert type(index)      is int and index >= 0
    assert type(byColumn)   is bool
    assert index < matrix.Height if byColumn == False else index < matrix.Width

    matrixData  = theMatrix.get_data()
    result      = []

    if byColumn == False:
      for i in matrixData[index]: result.append(i)
    else:
      for i in range(theMatrix.Height): result.append(matrixData[i][index])

    return vector.Vector(result)
