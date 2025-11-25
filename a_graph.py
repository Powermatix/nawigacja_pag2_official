# creates dict-graph from .shp file
# to use astar see wrapper.py
# .shx needs to be in the same directory

import shapely
from pyogrio.errors import DataSourceError
import geopandas as gpd
from math import inf

ID = 0

def generate_id():
    global ID
    ID += 1
    return ID

# different default case
def get_weight(length, road_class):
    if road_class == 'NA':
        w = length/50
    else:
        w = length/road_class
    if w < 0:
        print("WARNING: negative weight!!!!1! ABORT with ctrl-c")
    return w

roadClasses = {'droga wewnętrzna': 20, 'droga dojazdowa': 30, 'droga lokalna': 50, 'droga zbiorcza': 70, 'droga główna': 70, 'droga główna ruchu przyśpieszonego': 100, 'droga ekspresowa': 120, 'autostrada': 140, 'A':140,'S':120,'GP':100,'G':70,'Z':70,'L':50,'D':30,'I':20}

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
            add_edge(nodes, edges, tuple(round(val, 0) for val in line.geometry.coords[0]), tuple(round(val, 0) for val in line.geometry.coords[-1]), get_weight(lineLength, "NA"))

    else:
        colName = colNameIntersection.pop()
        for line in lines.itertuples():
            lineLength = shapely.length(line.geometry)
            add_edge(nodes, edges, tuple(round(val, 0) for val in line.geometry.coords[0]), tuple(round(val, 0) for val in line.geometry.coords[-1]), get_weight(lineLength, roadClasses[getattr(line, colName)]))
    return nodes, edges

# will overwrite duplicate nodes - not fixed, because add_edge will discard duplicate nodes prior
def add_node(nodes, node_id: str, x:float = 0.0, y:float = 0.0):
    nodes[node_id] = {
                        "x" : x,
                        "y" : y,
                        "g" : inf,
                        "h" : inf,
                        "f" : inf,
                        "p" : None
                        }

# supports edge_ids now
def add_edge(nodes, edges, from_node: tuple[float, float], to_node: tuple[float, float], weight: float):
    node_id1 = '_'.join(str(val) for val in from_node)
    node_id2 = '_'.join(str(val) for val in to_node)

    if node_id1 not in nodes.keys():
        add_node(nodes, node_id1, from_node[0], from_node[1])
    if node_id2 not in nodes.keys():
        add_node(nodes, node_id2, to_node[0], to_node[1])

    edge_id1 = generate_id()

    edges[edge_id1] = {
                             "s" : node_id1,
                             "e" : node_id2,
                             "w" : weight
                            }

    # uncomment for bidirectional
    edge_id2 = generate_id()
    edges[edge_id2] = {
                             "s" : node_id2,
                             "e" : node_id1,
                             "w" : weight
                            }

if __name__ == "__main__":
    nodes, edges = make_dict("shp/drogi.shp")
    # print(edges)
    # print(nodes)
