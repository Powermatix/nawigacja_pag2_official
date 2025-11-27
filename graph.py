from typing import Dict, List, Tuple
import math


class Node:
    def __init__(self,x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

        #atrybuty przechowujące wartości wykorzystywane w A*
        self.g = math.inf
        self.h = math.inf
        self.f = math.inf

        #wierzchołek poprzedzający znajdowany w A*
        self.p = None

        # wybrana przez algorytm krawędź grafu
        # (w przypadku gdy między wierzchołkami jest więcej niż jedna)
        self.e = None

    
class Edge:
    def  __init__(self,edge_id: int, from_node: str, to_node: str, weight:float, length:float):
        self.edge_id = edge_id
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.length = length


class Graph:

    def __init__(self):
        self.nodes: Dict[str, Node ] = {}
        self.edges: Dict[str, List[Edge]] = {}

        # licznik do nadawania identyfikatorów dla krawędzi
        self.edge_id_count = 0

        # do przechowywania prawdziwego przebiegu krawędzi
        self.edge_geometries: Dict[int, List[tuple[float]]] = {}

    def add_node(self, node_id: str, x:float = 0.0, y:float = 0.0) -> Node:
        if node_id not in self.nodes:
            node = Node(x, y)
            self.nodes[node_id] = node
            self.edges[node_id] = []
            return node
        return self.nodes[node_id]

    def add_edge(self, from_node: tuple[float, float], to_node: tuple[float, float], weight: float, length:float, all_nodes,
                 bidirectional: bool = True):
        from_nodeId = '_'.join(str(val) for val in from_node)
        to_nodeId = '_'.join(str(val) for val in to_node)
        if from_node not in self.nodes:
            self.add_node(from_nodeId, from_node[0], from_node[1])
        if to_node not in self.nodes:
            self.add_node(to_nodeId, to_node[0], to_node[1])

        edge = Edge(self.edge_id_count,from_nodeId, to_nodeId, weight, length)
        self.edge_geometries[self.edge_id_count] = all_nodes
        self.edge_id_count += 1
        self.edges[from_nodeId].append(edge)

        if bidirectional:
            # reverse_edge = Edge(self.edge_id_count,to_nodeId, from_nodeId, weight,length,nodes)
            # self.edge_id_count += 1
            self.edges[to_nodeId].append(edge)

    def get_neighbors(self, node_id:str) -> List[Tuple[int,str,float,float]]:
        if node_id not in self.edges:
            return []
        neighbors = []
        for edge in self.edges[node_id]:
            other_node = edge.to_node if edge.to_node != node_id else edge.from_node
            neighbors.append((edge.edge_id, other_node, edge.weight, edge.length))
        return neighbors

    def get_node(self, node_id:str) -> Node:
        return self.nodes.get(node_id)

    def get_edge_geometry(self, edge_id: int) -> List[tuple[float]]:
        return self.edge_geometries[edge_id]

    def distance(self, node1_id: str, node2_id: str) -> float:
        return math.sqrt((self.nodes[node1_id].x - self.nodes[node2_id].x) ** 2 + (
                    self.nodes[node1_id].y - self.nodes[node2_id].y) ** 2)