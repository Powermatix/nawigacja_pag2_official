# implements:
#   -graph class
#   -undirected graph matplotlib visualisation
#   -directed and undirected path visualisation
# also:
#   -graph creation instructions
#   -graph text representation
#   -misc utility functions

# status: works ig, assuming input is correct, little testing done, needs data
# structure optimisation -> passing too much info in functions
# possible solution: move functions with arguments like vertices, edges etc
# inside graph class to limit passing data as arguments
# TODO dicts/hash tables
# problem: when graphing, edges have to "ask" vertices where they end
# linear search everywhere. inefficient
# problem: no separation of graph class and plots
# TODO split into modules

# TODO test with other graph examples, make testing module
# TODO agree on argument/function naming scheme
# TODO distance function, weight function, store weights in dict id-weight?
# TODO change colors in matplotlib, add grid

import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, vertex_id, vertex_x, vertex_y, vertex_weight):
        self.vertex_id = vertex_id
        self.vertex_x = vertex_x
        self.vertex_y = vertex_y
        self.vertex_weight = vertex_weight
    def __repr__(self):
        return f"Vertex(id={self.vertex_id},\tx={self.vertex_x},\ty={self.vertex_y},\tw={self.vertex_weight})"


# edge_from and edge_to are vertex_ids
class Edge:
    def __init__(self, edge_id, edge_from, edge_to, edge_weight):
        self.edge_id = edge_id
        self.edge_from = edge_from
        self.edge_to = edge_to
        self.edge_weight = edge_weight
    def __repr__(self):
        return f"Edge(id={self.edge_id},\tfrom={self.edge_from},\tto={self.edge_to},\tw={self.edge_weight})"


# TODO add/delete vertices/edges
# TODO check validity of graph structure in init
# TODO resolve duplicate paths, remove loops here?
class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
    def __repr__(self):
        temp = "Graph(\n"
        for i in self.vertices:
            temp += i.__repr__()+",\n"
        temp +="\n"
        for i in self.edges:
            temp += i.__repr__()+",\n"
        temp +=")\n"
        return temp


# vertices is a list ("database") of all vertices, path_vertex_ids shows path
class Path:
    def __init__(self, vertices, path_vertex_ids):
        self.vertices = vertices
        self.path_vertex_ids = path_vertex_ids


# example: generate_ids(0,3) -> [0,1,2]
def generate_ids(start, number):
    return [ i for i in range(start, start+number)]

def find_edge_start_and_end(edge, vertices): #in coordinates
    start_id = edge.edge_from
    end_id = edge.edge_to
    for vertex in vertices:
        if vertex.vertex_id == start_id:
            start_x = vertex.vertex_x
            start_y = vertex.vertex_y
            break
    for vertex in vertices:
        if vertex.vertex_id == end_id:
            end_x = vertex.vertex_x
            end_y = vertex.vertex_y
            break
    return start_x, start_y, end_x, end_y

def find_vertex_coordinates(vertex_id, vertices): #given vertex_id
    for vertex in vertices:
        if vertex.vertex_id == vertex_id:
            vertex_x = vertex.vertex_x
            vertex_y = vertex.vertex_y
            break
    return vertex_x, vertex_y

# assumes undirected
def find_vertex_neighbors(vertices, edges, vertex_id):
    neighbor_ids = []
    for edge in edges:
        if (edge.vertex_from == vertex_id):
            neighbor_ids.append(vertex_from)
        if (edge.vertex_to == vertex_id):
            neighbor_ids.append(vertex_to)
    return neighbor_ids

def create_vertices(ids, xs, ys, weights):
    vertices = []
    for i in zip(ids,xs,ys,weights):
        vertices.append(Vertex(i[0],i[1],i[2],i[3]))
    return vertices

def create_edges(ids, froms, tos, weights):
    edges = []
    for i in zip(ids,froms, tos, weights):
        edges.append(Edge(i[0],i[1],i[2],i[3]))
    return edges

def plot_vertex(vertex):
    plt.plot([vertex.vertex_x], [vertex.vertex_y], marker = 'o')
    plt.text(vertex.vertex_x, vertex.vertex_y, '{}'.format(vertex.vertex_id), fontsize=9, ha='right')

def plot_vertices(vertices):
    for i in vertices:
        plot_vertex(i)

def plot_edge(edge, vertices):
    start_x, start_y, end_x, end_y = find_edge_start_and_end(edge,vertices)
    plt.plot([start_x,end_x],[start_y,end_y])
    plt.text((start_x+end_x)/2, (end_x+end_y)/2, '{}'.format(edge.edge_id), fontsize=9, ha='right')

def plot_edges(edges,vertices):
    for edge in edges:
        plot_edge(edge,vertices)

def plot_graph(graph):
    plot_edges(graph.edges,graph.vertices)
    plot_vertices(graph.vertices)

def plot_directed_path(path):
    for i in range(len(path.path_vertex_ids)-1):
        start_x, start_y = find_vertex_coordinates(path.path_vertex_ids[i], path.vertices)
        next_x, next_y = find_vertex_coordinates(path.path_vertex_ids[i+1], path.vertices)
        plt.annotate('', xy=(next_x, next_y), xytext=(start_x, start_y), arrowprops=dict(facecolor='blue', shrink=0.01))

def plot_undirected_path(path):
    for i in range(len(path.path_vertex_ids)-1):
        start_x, start_y = find_vertex_coordinates(path.path_vertex_ids[i], path.vertices)
        next_x, next_y = find_vertex_coordinates(path.path_vertex_ids[i+1], path.vertices)
        plt.plot([start_x, next_x], [start_y, next_y])

# how to create vertices, edges and graphs:
vertices_ids = ["v0", "v1", "v2", "v3"]
vertices_xs = [0, 5, -2, 7]
vertices_ys = [-10, 13, 5, 2]
vertices_weights = [1, 2, 3, 4]

edges_ids = ["e1", "e2", "e3", "e4"]
edges_froms = ["v0", "v3", "v2", "v1"]
edges_tos = ["v3", "v1", "v1", "v0"]
edges_weights = [1, 2, 3, 4]

my_vertices = create_vertices(vertices_ids, vertices_xs, vertices_ys, vertices_weights)
my_edges = create_edges(edges_ids, edges_froms, edges_tos, edges_weights)
my_graph = Graph(my_vertices, my_edges)
my_path = Path(my_vertices, ["v0", "v1", "v2", "v3"])

print(my_graph)
# TODO repr print(my_path)

# demo1:
plot_graph(my_graph)
plt.show()

# demo2:
plot_vertices(my_graph.vertices)
plot_directed_path(my_path)
plt.show()

# demo3:
plot_vertices(my_graph.vertices)
plot_undirected_path(my_path)
plt.show()
