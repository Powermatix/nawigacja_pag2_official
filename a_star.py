from graph import *
import heapq

# tylko do debugowania
PRINT = False

def heuristic(node_id1 : str, node_id2 : str, nodes):
    sx, sy = node_id1.split('_')
    ex, ey = node_id2.split('_')
    # sx, sy = nodes[node_id1].x,nodes[node_id1].y
    # sx, sy = nodes[node_id2].x,nodes[node_id2].y
    return round((float(sx)-float(ex))**2+(float(sy)-float(ey))**2)**0.5


def astar(start_id, end_id, in_graph : Graph, shortest=False):
    global PLOT
    global PLOT_EXT
    global PRINT

    nodes = in_graph.nodes

    g = 0
    h = heuristic(start_id, end_id, nodes)
    f = g+h

    open_lst = [[0, start_id]]
    heapq.heapify(open_lst)

    closed_lst = []

    nodes[start_id].g = 0
    nodes[start_id].h = h
    nodes[start_id].f = f
    nodes[start_id].p = None
    nodes[start_id].e = None

    # liczba oznaczająca indeks pod którym znajduje się odpowiednia
    # waga (inna dla trasy najkrótszej, inna dla najszybszej)
    # zwrócona przez get_neighbors(id) w algorytmie
    edge_weight_idx = 2
    if shortest:
        edge_weight_idx = 3

    while open_lst:
        current_id = heapq.heappop(open_lst)[1]
        if PRINT:
            print(f'current: {current_id}')
        
        # neighbor to tuple zawierający: (edge_id, neighbor_id, neighbor_weight, neighbor_length)
        for neighbor in in_graph.get_neighbors(current_id):
            if PRINT:
                print(f"\tneighbor:{neighbor[1]}, {neighbor[edge_weight_idx]}")
            if neighbor[1] == end_id:
                # if PLOT:
                #     plot_edges(edges,nodes)
                #     plot_nodes_color(nodes, current_id, open_lst, closed_lst)
                #     plt.show()

                all_nodes = [node[1] for node in open_lst]
                all_nodes += closed_lst
                for node_id in all_nodes:
                    nodes[node_id].g = math.inf
                    nodes[node_id].h = math.inf
                    nodes[node_id].f = math.inf


                nodes[neighbor[1]].p = current_id
                nodes[neighbor[1]].e = neighbor[0]
                return reconstruct_path(neighbor[1], nodes)
            else:
                g = nodes[current_id].g + neighbor[edge_weight_idx]
                h = heuristic(neighbor[1],end_id,nodes)
                f = g+h
                if f > nodes[neighbor[1]].f:
                    if PRINT:
                        print(f"\t\tcase: not opt")
                        print(f"{f},{nodes[neighbor[1]].f}")
                elif neighbor[1] in closed_lst:
                    if PRINT:
                        print(f"\t\tcase: closed")
                else:
                    heapq.heappush(open_lst,[f,neighbor[1]])
                    nodes[neighbor[1]].g = g
                    nodes[neighbor[1]].h = h
                    nodes[neighbor[1]].f = f
                    nodes[neighbor[1]].p = current_id
                    nodes[neighbor[1]].e = neighbor[0]
                    if PRINT:
                        print(f"\t\tcase: update")
        closed_lst.append(current_id)
        if PRINT:
            print(f"open: {open_lst}")
            print(f"closed: {closed_lst}")
        # if PLOT_EXT:
        #     plot_edges(edges,nodes)
        #     plot_nodes_color(nodes, current_id, open_lst, closed_lst)
        #     plt.show()
    if PRINT:
        print("FAIL")
    return None

# wynikiem algorytmu jest lista odwiedzonych wierzchołków zawierająca
# oprócz id wierzchołka także id krawędzi po której nastąpił ruch
def reconstruct_path(current_id, nodes):
    path = []
    while current_id is not None:
        path.insert(0, (current_id, nodes[current_id].e))
        current_id = nodes[current_id].p
    return path

