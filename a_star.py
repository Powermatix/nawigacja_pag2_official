from graph import *
import heapq

# tylko do debugowania
PRINT = False

def heuristic(node_id1 : str, node_id2 : str, dijkstra=False):
    if dijkstra:
        return 0
    sx, sy = node_id1.split('_')
    ex, ey = node_id2.split('_')
    # sx, sy = nodes[node_id1].x,nodes[node_id1].y
    # ex, ey = nodes[node_id2].x,nodes[node_id2].y
    return round((float(sx)-float(ex))**2+(float(sy)-float(ey))**2)**0.5


def astar(start_id, end_id, in_graph : Graph, shortest=False, dijkstra=False):
    global PLOT
    global PLOT_EXT
    global PRINT


    g = 0
    h = heuristic(start_id, end_id, dijkstra)
    f = g+h

    gValues = {}
    fValues = {}
    lastNodeEdge = {}

    open_lst = [[f, start_id]]
    heapq.heapify(open_lst)

    closed_lst = []

    gValues[start_id] = 0
    fValues[start_id] = f
    lastNodeEdge[start_id] = (None,None)


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
        if current_id == end_id:
            return reconstruct_path(current_id,lastNodeEdge)
        # neighbor to tuple zawierający: (edge_id, neighbor_id, neighbor_weight, neighbor_length)
        for neighbor in in_graph.get_neighbors(current_id):
            if PRINT:
                print(f"\tneighbor:{neighbor[1]}, {neighbor[edge_weight_idx]}")
                # if PLOT:
                #     plot_edges(edges,nodes)
                #     plot_nodes_color(nodes, current_id, open_lst, closed_lst)
                #     plt.show()
            neighbor_id = neighbor[1]

            g = gValues[current_id] + neighbor[edge_weight_idx]
            h = heuristic(neighbor_id,end_id, dijkstra)
            f = g+h

            if g > gValues.get(neighbor_id,math.inf):
                if PRINT:
                    print(f"\t\tcase: not opt")
                    print(f"{f},{gValues[neighbor_id]}")
            elif neighbor_id in closed_lst:
                if PRINT:
                    print(f"\t\tcase: closed")
            else:
                heapq.heappush(open_lst,[f,neighbor_id])
                gValues[neighbor_id] = g
                fValues[neighbor_id] = f

                lastNodeEdge[neighbor_id] = (current_id,neighbor[0])
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
def reconstruct_path(current_id,lastNodeEdge):
    path = []
    while current_id is not None:
        edge_id = lastNodeEdge[current_id][1]
        path.insert(0, (current_id, edge_id))
        current_id = lastNodeEdge[current_id][0]
    return path

def astar_wrapper(start_id, end_id, in_graph : Graph, shortest=False):
    path = astar(start_id,end_id,in_graph,shortest)
    if path is None:
        return None
    coords = [in_graph.get_edge_geometry(val[1]) for val in path[1:]]
    return coords

