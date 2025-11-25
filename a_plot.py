import matplotlib.pyplot as plt
from math import inf

# error fix:
import matplotlib
matplotlib.use('Qt5Agg')

# key, value of node.items(), function made only for use in plot_nodes()
def plot_node(key, value, color):
    plt.plot([value['x']], [value['y']], mfc = color, mec = color, marker = 's', ms = 20)
    g = inf if value['g'] == inf else round(value['g'],1)
    h = inf if value['h'] == inf else round(value['h'],1)
    f = inf if value['f'] == inf else round(value['f'],1)
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
