# dict version of makeGraph.py for use in searching
# TODO make modules for astar and demos

import shapely
from pyogrio.errors import DataSourceError
from astar import *
import geopandas as gpd

roadClasses = {'droga wewnętrzna': 20, 'droga dojazdowa': 30, 'droga lokalna': 50, 'droga zbiorcza': 70,
               'droga główna': 70, 'droga główna ruchu przyśpieszonego': 100, 'droga ekspresowa': 120, 'autostrada': 140,
               'A':140,'S':120,'GP':100,'G':70,'Z':70,'L':50,'D':30,'I':20}

columnNames = {'klasa_drogi', 'klasa_drog', 'klasadrogi'}

def make_dict(shapePath: str):
    try:
        lines = gpd.read_file(shapePath)
    except DataSourceError:
        print("Błąd odczytu pliku")
        return None

    edges = {}
    nodes = {}

    lines.columns = lines.columns.str.lower()

    if 'geometry' not in lines.columns:
        print('Brak geometrii')
        return None

    colNameIntersection = columnNames.intersection(list(lines.columns))
    if len(colNameIntersection) == 0:
        print('Brak informacji o klasie drogi')

        for line in lines.itertuples():
            lineLength = shapely.length(line.geometry)
            add_edge(nodes, edges, tuple(round(val, 0) for val in line.geometry.coords[0]),
                           tuple(round(val, 0) for val in line.geometry.coords[-1]),
                           lineLength)

    else:
        colName = colNameIntersection.pop()
        for line in lines.itertuples():
            lineLength = shapely.length(line.geometry)
            add_edge(nodes, edges, tuple(round(val, 0) for val in line.geometry.coords[0]),
                           tuple(round(val, 0) for val in line.geometry.coords[-1]),
                           lineLength / roadClasses[getattr(line, colName)])

    return nodes, edges

# almost the same usage, diff: nodes, no name
# will overwrite duplicate nodes
# not fixed, because add_edge will discard duplicate nodes prior
def add_node(nodes, node_id: str, x:float = 0.0, y:float = 0.0):
    nodes[node_id] = {
                        "x" : x,
                        "y" : y,
                        "g" : math.inf,
                        "h" : math.inf,
                        "f" : math.inf,
                        "p" : None
                        }

# almost the same usage, diff: nodes, no name (can add dummy name parameter)
def add_edge(nodes, edges, from_node: tuple[float, float], to_node: tuple[float, float], weight: float):
    node_id1 = '_'.join(str(val) for val in from_node)
    node_id2 = '_'.join(str(val) for val in to_node)

    if node_id1 not in nodes.keys():
        add_node(nodes, node_id1, from_node[0], from_node[1])
    if node_id2 not in nodes.keys():
        add_node(nodes, node_id2, to_node[0], to_node[1])

    # diff: generating edge_ids
    # TODO allow duplicate edges by generating unique ids
    # TODO add every edge 2 times to simulate bidirectionality
    edge_id = '_'.join(str(val) for val in [node_id1, node_id2])
    edges[edge_id] = {
                             "s" : node_id1,
                             "e" : node_id2,
                             "w" : weight
                            }

if __name__ == "__main__":
    nodes, edges = make_dict("drogi.shp")
    plot_edges(edges, nodes)
    plot_nodes(nodes)
    plt.show()
