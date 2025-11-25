# edges : edge_id = {s,e,w} s,e are node_ids, w is float/inf
# nodes : node_id = {x,y,g,h,f,p} p is node_id or None, other float/inf

# seems solved? green node on demo does not always have correct f value rendered TODO

# TODO remove plotting for the final version (choice)
# for now, set manually here
PLOT = True # this is plotting the before and after
PLOT_EXT = True # this is plotting the intermediate steps
PRINT = True

from a_plot import *
import heapq

# comment out for dijkstra
def heuristic(node_id1,node_id2, nodes):
    sx = nodes[node_id1]['x']
    sy = nodes[node_id1]['y']
    ex = nodes[node_id2]['x']
    ey = nodes[node_id2]['y']
    return round((sx-ex)**2+(sy-ey)**2)**0.5
    #return 0

# duplicate edges ok
def node2neighbors(node_id, edges):
    wn = [ [value["w"], value["e"]] for key, value in edges.items() if value["s"] == node_id ]
    # weight = 0, node_id = 1
    return wn

# now returns None on fail
def astar(start_id, end_id, nodes, edges):
    global PLOT
    global PLOT_EXT
    global PRINT

    if PLOT:
        plot_edges(edges,nodes)
        plot_nodes(nodes)
        plt.show()

    g = 0
    h = heuristic(start_id, end_id, nodes)
    f = g+h

    open_lst = [[0, start_id]]
    heapq.heapify(open_lst)

    closed_lst = []

    nodes[start_id]["g"] = 0 
    nodes[start_id]["h"] = h
    nodes[start_id]["f"] = f
    nodes[start_id]["p"] = None

    while open_lst:
        current_id = heapq.heappop(open_lst)[1]
        if PRINT:
            print(f'current: {current_id}')
        for nw in node2neighbors(current_id,edges):
            if PRINT:
                print(f"\tneighbor:{nw[1]}, {nw[0]}")
            if nw[1] == end_id:
                if PLOT:
                    plot_edges(edges,nodes)
                    plot_nodes_color(nodes, current_id, open_lst, closed_lst)
                    plt.show()
                return reconstruct_path(current_id, nodes)
            else:
                g = nodes[current_id]['g'] + nw[0]
                h = heuristic(nw[1],end_id,nodes)
                f = g+h
                if f > nodes[nw[1]]['f']:
                    if PRINT:
                        print(f"\t\tcase: not opt")
                        print(f"{f},{nodes[nw[1]]['f']}")
                elif nw[1] in closed_lst:
                    if PRINT:
                        print(f"\t\tcase: closed")
                else:
                    heapq.heappush(open_lst,[f,nw[1]])
                    nodes[nw[1]]['g'] = g
                    nodes[nw[1]]['h'] = h
                    nodes[nw[1]]['f'] = f
                    nodes[nw[1]]['p'] = current_id
                    if PRINT:
                        print(f"\t\tcase: update")
        closed_lst.append(current_id)
        if PRINT:
            print(f"open: {open_lst}")
            print(f"closed: {closed_lst}")
        if PLOT_EXT:
            plot_edges(edges,nodes)
            plot_nodes_color(nodes, current_id, open_lst, closed_lst)
            plt.show()
    if PRINT:
        print("FAIL")
    return None

def reconstruct_path(current_id, nodes):
    path = []
    while current_id is not None:
        path.insert(0, current_id)
        current_id = nodes[current_id]['p']
    return path
