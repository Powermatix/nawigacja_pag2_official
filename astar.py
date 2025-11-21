# base, inefficient version of a* and dijkstra
# edge weights should be calculated separately
# ex. tweak weight calculating function to favour highways
# edges : edge_id = {s,e,w} s,e are node_ids, w is float/inf
# nodes : node_id = {x,y,g,h,f,p} p is node_id or None, other float, ghf also inf
# important: ensure non-negative edge weights
# possible: separate fields for class, name, etc
# preferably in edges_extra : edge_id : {extra info}
# TODO rethink data structures
# green node on demo does not always have correct f value rendered TODO
# TODO test with make_graph (dictionary)

import random
import math
import matplotlib.pyplot as plt

# error fix:
import matplotlib
matplotlib.use('Qt5Agg')

# comment out for dijkstra (temporary)
def heuristic(node_id1,node_id2, nodes):
    sx = nodes[node_id1]['x']
    sy = nodes[node_id1]['y']
    ex = nodes[node_id2]['x']
    ey = nodes[node_id2]['y']
    return round((sx-ex)**2+(sy-ey)**2)**0.5
    #return 0

# this assumes no duplicate edges, TODO replace and delete
# better approach below
def get_weight_between(node_id1, node_id2, edges):
    for key, value in edges.items():
        if value.get("s") == node_id1 and value.get("e") == node_id2:
            return value.get("w") 

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
                                "g" : math.inf,
                                "h" : math.inf,
                                "f" : math.inf,
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


# key, value of node.items(), function made only for plot_nodes()
def plot_node(key, value, color):
    plt.plot([value['x']], [value['y']], mfc = color, mec = color, marker = 's', ms = 20)
    g = math.inf if value['g'] == math.inf else round(value['g'],1)
    h = math.inf if value['h'] == math.inf else round(value['h'],1)
    f = math.inf if value['f'] == math.inf else round(value['f'],1)
    #f = value['f']
    plt.text(value['x'],value['y'],'{}\n{}|{}|{}'.format(key, g, h, f), fontsize=8, ha = 'center', va = 'center')

def plot_nodes(nodes):
    for key,value in nodes.items():
        plot_node(key,value,'gray')

# y = open, r = closed, g = current, gray = unvisited
def plot_nodes_color(nodes, current_id, open_lst, closed_lst):
    for key,value in nodes.items():
        if key == current_id:
            plot_node(key,value,'g')
        elif any(key in sublist for sublist in open_lst):
            plot_node(key,value,'y')
        elif key in closed_lst:
            plot_node(key,value,'r')
        else:
            plot_node(key,value,'gray')

# key, value of edge.items(), again for use with plot_edges
# only for consistency with above
def plot_edge(key, value, nodes):
    sx = nodes[value["s"]]["x"]
    sy = nodes[value["s"]]["y"]
    ex = nodes[value["e"]]["x"]
    ey = nodes[value["e"]]["y"]
    plt.plot([sx,ex],[sy,ey], '#888888')
    #plt.text((start_x+end_x)/2,(start_y+end_y)/2,'{}'.format(value["dist"]), fontsize=9, ha = 'center', va = 'center')

def plot_edges(edges, nodes):
    for key,value in edges.items():
        plot_edge(key,value,nodes)

# replace get weight function by this TODO, store weights in w
def node2neighbors(node_id, edges):
    n1 = [value["e"] for key, value in edges.items() if value["s"] == node_id]
    # store w = [...] or [[e1-w1], ..., [en-wn]]
    return(n1)

def sort_list(lst):
    return sorted(lst, key=lambda x: x[0])

def astar(start_id, end_id, nodes, edges):

    plot_edges(edges,nodes)
    plot_nodes(nodes)
    plt.show()

    # init lists, starting values for start_id
    g = 0
    h = heuristic(start_id, end_id, nodes)
    f = g + h

    # TODO heapq
    open_lst = [[f, start_id]]
    closed_lst = []

    nodes[start_id]["g"] = 0 
    nodes[start_id]["h"] = h
    nodes[start_id]["f"] = f
    nodes[start_id]["p"] = None

    while open_lst:
        # get node with lowest f value
        open_lst = sort_list(open_lst)
        current_id = open_lst[0][1]
        print(f'current: {current_id}')
        print(f'\topen: {open_lst}')
        # check with other pseudocode variants TODO
        if current_id == end_id:
            return reconstruct_path(current_id, nodes)
        # remove current_id
        open_lst = [sublist for sublist in open_lst if sublist[1] != current_id] 
        closed_lst.append(current_id)
        for neighbor_id in node2neighbors(current_id,edges):
            print(f"\tneighbor:{neighbor_id}")
            if neighbor_id in closed_lst:
                print(f"\t\tcase: closed")
                continue
            g = nodes[current_id]['g'] + get_weight_between(current_id, neighbor_id, edges)
            h = heuristic(neighbor_id,end_id,nodes)
            if neighbor_id not in open_lst:
                open_lst.append([g+h, neighbor_id])
                print(f"\t\tupdated: open")
            elif g >= nodes[neighbor_id]['g']: 
                print(f"\t\tdiscarded route")
                continue
            nodes[neighbor_id]['p'] = current_id
            nodes[neighbor_id]['g'] = g
            nodes[neighbor_id]['h'] = h
            nodes[neighbor_id]['f'] = g+h
            print(f"\t\tupdated: graph")
        plot_edges(edges,nodes)
        plot_nodes_color(nodes, current_id, open_lst, closed_lst)
        plt.show()
    print("FAIL")
    return None
    # TODO value for fail? error?

def reconstruct_path(current_id, nodes):
    path = []
    while current_id is not None:
        path.insert(0, current_id)
        current_id = nodes[current_id]['p']
    return path

nodes, edges = generate_cartesian(1,1,6,6)
print(astar("1_1","6_6",nodes,edges))
