# astar init state visualisation
# obsoletes graph2.py
# TODO decrease graph load times

import random
import math
import matplotlib.pyplot as plt

# modify here to turn random deletion off
def random_function():
    return bool(random.getrandbits(1))

# modify here for ex. manhattan distance
def distance(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

# modify heuristic here (temporary)
# TODO arguments should be nodes
def heuristic(x1,y1,x2,y2):
    return round(distance(x1,y1,x2,y2))

nodes = {}
edges = {}

# generates cartesian grid graph
def generate_graph(min_x, min_y, max_x, max_y):

    # generate nodes
    for x in range(min_x,max_x+1):
        for y in range(min_y,max_y+1):
            nodes[f"{x}_{y}"] = {
                                "x" : x,
                                "y" : y,
                                "g" : math.inf, # current distance
                                "h" : math.inf, # heuristic
                                "p" : "" # parent
                                }

    # TODO possible opt to change dict structure from edges[id] = {from,to,dist} to edges[from][to] = dist
    # note: won't allow duplicate connections as from+to will be the key
    # note: probably will store duplicates (to+from, from+to), to reduce search times

    # generate edges
    for x in range(min_x,max_x+1):
        for y in range(min_y,max_y+1):
            if x < max_x and random_function(): # horizontal
                edges[f"e_{x}_{y}_h"] = {
                                        "from" : f"{x}_{y}",
                                        "to" : f"{x+1}_{y}",
                                        "dist" : 1.0
                                       }
            if y < max_y and random_function(): # vertical
                edges[f"e_{x}_{y}_v"] = {
                                        "from" : f"{x}_{y}",
                                        "to" : f"{x}_{y+1}",
                                        "dist" : 1.0
                                       }
            if x < max_x and y < max_y and random_function(): # diagonal 1
                edges[f"e_{x}_{y}_d1"] = {
                                        "from" : f"{x}_{y}",
                                        "to" : f"{x+1}_{y+1}",
                                        "dist" : 1.4
                                       }
            if x < max_x and y > min_y and random_function(): # diagonal 2
                edges[f"e_{x}_{y}_d2"] = {
                                        "from" : f"{x}_{y}",
                                        "to" : f"{x+1}_{y-1}",
                                        "dist" : 1.4
                                       }

generate_graph(1,1,4,4)

# key, value of node.items()
def plot_node(key, value, color):
    plt.plot([value['x']], [value['y']], mfc = color, mec = color, marker = 's', ms = 20)
    plt.text(value['x'],value['y'],'{}\n{}|{}'.format(key,value['g'],value['h']), fontsize=8, ha = 'center', va = 'center')

# TODO ensure no keys in both to_test and visited
def plot_nodes_color(nodes, nodes_to_test, nodes_visited):
    for key,value in nodes.items():
        if key in nodes_to_test:
            plot_node(key,value,'y')
        elif key in nodes_visited:
            plot_node(key,value,'g')
        else:
            plot_node(key,value,'r')

# key, value of edge.items()
def plot_edge(key, value, nodes):
    start_x = nodes[value["from"]]["x"]
    start_y = nodes[value["from"]]["y"]
    end_x = nodes[value["to"]]["x"]
    end_y = nodes[value["to"]]["y"]
    # plot distance or edges
    plt.plot([start_x,end_x],[start_y,end_y], '#888888')
    plt.text((start_x+end_x)/2,(start_y+end_y)/2,'{}'.format(value["dist"]), fontsize=9, ha = 'center', va = 'center')

def plot_edges(edges, nodes):
    for key,value in edges.items():
        plot_edge(key,value,nodes)

# note: can be easilly modified to return edges
def node2neighbors(node_id, edges):
    n1 = [value["to"] for key, value in edges.items() if value["from"] == node_id]
    n2 = [value["from"] for key, value in edges.items() if value["to"] == node_id]
    print(n1 + n2)

# node2neighbors("2_2", edges)

def astar(start_id, end_id, nodes, edges):

    nodes_to_test = []
    nodes_visited = []

    nodes[start_id]["g"] = 0 
    nodes[start_id]["h"] = heuristic(nodes[start_id]["x"],nodes[start_id]["y"],nodes[end_id]["x"],nodes[end_id]["y"])

    nodes_to_test.append(start_id)

    plot_edges(edges,nodes)
    plot_nodes_color(nodes, nodes_to_test, nodes_visited)

    plt.show()

# TODO finish astar + step-by-step vis
''' while not reached dest:
        nodes_with_lowest_h = [k for k, v in nodes_to_test if h == min_val]
        choose some node

    for each neighbor of chosen:
        add them to test_nodes
        if their node.h < a.local + dist
            update p
            update g
            update h
            update them in test_nodes with h
    delete neighbor from test nodes

    show plot
'''

astar("2_2","4_4",nodes,edges)
