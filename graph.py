from typing import Dict, List, Tuple
import math
class Node:
    def __init__(self, node_id: str , x: float = 0.0, y: float = 0.0, name: str="" ):
        self.id = node_id
        self.x = x
        self.y = y
        self.name = name or node_id

    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
class Edge:
    def  __init__(self, from_node: str, to_node: str, weight:float, name: str=""):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.name = name


class Graph:

    def __init__(self):
        self.nodes: Dict[str, Node ] = {}
        self.edges: Dict[str, List[Edge]] = {}

    def add_node(self, node_id: str, x:float = 0.0, y:float = 0.0, name: str="") -> Node:
        if node_id not in self.nodes:
            node= Node(node_id, x, y, name)
            self.nodes[node_id] = node
            self.edges[node_id] = []
            return node
        return self.nodes[node_id]

    def add_edge(self, from_node: tuple[float, float], to_node: tuple[float, float], weight: float, name: str = "",
                 bidirectional: bool = True):
        from_nodeId = '_'.join(str(val) for val in from_node)
        to_nodeId = '_'.join(str(val) for val in to_node)
        if from_node not in self.nodes:
            self.add_node(from_nodeId, from_node[0], from_node[1])
        if to_node not in self.nodes:
            self.add_node(to_nodeId, to_node[0], to_node[1])

        edge = Edge(from_nodeId, to_nodeId, weight, name)
        self.edges[from_nodeId].append(edge)

        if bidirectional:
            reverse_edge = Edge(to_nodeId, from_nodeId, weight, name)
            self.edges[to_nodeId].append(reverse_edge)

    def get_neighbors(self, node_id:str) -> List[Tuple[str,float]]:
        if node_id not in self.edges:
            return []
        return [(edge.to_node, edge.weight) for edge in self.edges[node_id]]

    def get_node(self, node_id:str) -> Node:
        return self.nodes.get(node_id)
    
    def distance(self, node1_id: str, node2_id: str) -> float:
        return math.sqrt((self.nodes[node1_id].x - self.nodes[node2_id].x) ** 2 + (
                    self.nodes[node1_id].y - self.nodes[node2_id].y) ** 2)