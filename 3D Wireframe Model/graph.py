import copy

class Vertex(object):
    """A class for storing vertex information."""

    def __init__(self, data):
        """The Vertex constructor. Use of non-primitive
        types for data parameter should be avoided."""

        self.Data       = data
        self.Visited    = False

    def get_data(self):
        """Returns a deep copy of the vertex data."""

        return copy.deepcopy(self.Data)

    def __str__(self):
        """Returns a string representation of the vertex."""

        return "Visited? " + str(self.Visited) + "\n" + str(self.Data)

class Graph(object):
    """A class for a non-directed, non-weighted graph."""

    def __init__(self):
        """The Graph constructor."""

        self._vertices      = []
        self._adjacency     = []
        self._handler       = self._default_visit

    @property
    def Size(self):      return len(self._vertices)
    @property
    def AdjacencyMatrix(self):  return copy.deepcopy(self._adjacency)

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""

        assert type(vertex) is Vertex

        self._vertices.append(vertex)

        self._adjacency.append([])
        for i in range(self.Size): 
            self._adjacency[self.Size - 1].append(False)
        for i in range(self.Size - 1):
            self._adjacency[i].append(False)
      
    def delete_vertex(self, index):
        """Delete a vertex from the graph."""

        assert type(index) is int and index < self.Size

        self._adjacency.remove(self._adjacency[index])
        for i in self._adjacency:
            i.remove(i[index])
    
        self._vertices.remove(self._vertices[index])

    def add_edge(self, start, end):
        """Add an edge to the graph."""

        assert type(start)  is int and start    >= 0 and start  < self.Size
        assert type(end)    is int and end      >= 0 and end    < self.Size 

        self._adjacency[start][end] = True
        self._adjacency[end][start] = True
    
    def delete_edge(self, start, end):
        """Remove an edge from the graph. Returns true if 
        there is an edge to remove and false otherwise."""
    
        assert type(start)  is int and start    >= 0 and start  < self.Size
        assert type(end)    is int and end      >= 0 and end    < self.Size
    
        if self._adjacency[start][end] == False:
      
            return False
    
        self._adjacency[start][end] = False
        self._adjacency[end][start] = False
    
        return True
    
    def get_vertex(self, index):
        """Returns the vertex at the specified index."""

        assert type(index) is int and index >= 0 and index < self.Size

        return self._vertices[index]

    def _default_visit(self, index):
        """The defualt visitation handler. Prints a string representation
        of the vertex data."""

        assert type(index) is int and index >= 0 and index < self.Size

        print(self._vertices[index].get_data())

    def get_copy(self):
        """Returns a deep copy of the graph."""

        graphCopy = Graph()

        for vertex in self._vertices:
            graphCopy.add_vertex(Vertex(vertex.get_data()))

        for i in range(self.Size):
            for j in range(i + 1, self.Size):
                if self._adjacency[i][j] == True:
                    graphCopy.add_edge(i, j)

        return graphCopy
      
    def get_adjacent_unvisited(self, i):
        """Returns the index of an unvisited vertex adjacent to the one specified."""

        assert type(i) is int and i >= 0 and i < self.Size

        for j in range(self.Size):
            if self._adjacency[i][j] == True and self._vertices[j].Visited == False:

                return j

        return None

    def depth_first_search(self):
        """Performs a depth-first search on the entire graph."""

        self._vertices[0].Visited = True
        self._handler(0)
    
        #Finish later.
