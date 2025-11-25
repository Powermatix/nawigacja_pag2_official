import random
from math import inf

# generation of cartesian-like graph for testing/demonstration
def generate_cartesian(min_x, min_y, max_x, max_y):
    nodes = {}
    edges = {}
    # generate nodes, g = distance travelled so far, h = heuristic, f = g + h, p = parent
    for x in range(min_x,max_x+1):
        for y in range(min_y,max_y+1):
            nodes[f"{x}_{y}"] = {
                                "x" : x,
                                "y" : y,
                                "g" : inf,
                                "h" : inf,
                                "f" : inf,
                                "p" : None
                                }

    # generate edges s = start, e = end, w = weight
    # edges are added in xy and yx order to create bidirectional graph
    # note, the graph can be sigle directional
    for x in range(min_x,max_x+1):
        for y in range(min_y,max_y+1):
            if x < max_x and bool(random.getrandbits(1)): # horizontal
                edges[f"e_{x}_{y}_h"] = {
                                        "s" : f"{x}_{y}",
                                        "e" : f"{x+1}_{y}",
                                        "w" : 1.0
                                       }
                edges[f"e_{x}_{y}_hr"] = {
                                        "e" : f"{x}_{y}",
                                        "s" : f"{x+1}_{y}",
                                        "w" : 1.0
                                       }
            if y < max_y and bool(random.getrandbits(1)): # vertical
                edges[f"e_{x}_{y}_v"] = {
                                        "s" : f"{x}_{y}",
                                        "e" : f"{x}_{y+1}",
                                        "w" : 1.0
                                       }
                edges[f"e_{x}_{y}_vr"] = {
                                        "e" : f"{x}_{y}",
                                        "s" : f"{x}_{y+1}",
                                        "w" : 1.0
                                       }
            if x < max_x and y < max_y and bool(random.getrandbits(1)): # diagonal 1
                edges[f"e_{x}_{y}_d1"] = {
                                        "s" : f"{x}_{y}",
                                        "e" : f"{x+1}_{y+1}",
                                        "w" : 1.4
                                       }
                edges[f"e_{x}_{y}_d1r"] = {
                                        "e" : f"{x}_{y}",
                                        "s" : f"{x+1}_{y+1}",
                                        "w" : 1.4
                                       }
            if x < max_x and y > min_y and bool(random.getrandbits(1)): # diagonal 2
                edges[f"e_{x}_{y}_d2"] = {
                                        "s" : f"{x}_{y}",
                                        "e" : f"{x+1}_{y-1}",
                                        "w" : 1.4
                                       }
                edges[f"e_{x}_{y}_d2r"] = {
                                        "e" : f"{x}_{y}",
                                        "s" : f"{x+1}_{y-1}",
                                        "w" : 1.4
                                       }
    return(nodes, edges)
    
