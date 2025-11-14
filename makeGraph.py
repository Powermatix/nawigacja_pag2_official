import shapely
from pyogrio.errors import DataSourceError
from graph import Graph
import geopandas as gpd

roadClasses = {'droga wewnętrzna': 20, 'droga dojazdowa': 30, 'droga lokalna': 50, 'droga zbiorcza': 70,
               'droga główna': 70, 'droga główna ruchu przyśpieszonego': 100, 'droga ekspresowa': 120, 'autostrada': 140,
               'A':140,'S':120,'GP':100,'G':70,'Z':70,'L':50,'D':30,'I':20}

columnNames = {'klasa_drogi', 'klasa_drog', 'klasadrogi'}


def makeGraph(shapePath: str):
    try:
        lines = gpd.read_file(shapePath)
    except DataSourceError:
        print("Błąd odczytu pliku")
        return None

    graph = Graph()

    lines.columns = lines.columns.str.lower()

    if 'geometry' not in lines.columns:
        print('Brak geometrii')
        return None

    colNameIntersection = columnNames.intersection(list(lines.columns))
    if len(colNameIntersection) == 0:
        print('Brak informacji o klasie drogi')

        for line in lines.itertuples():
            lineLength = shapely.length(line.geometry)
            graph.add_edge(tuple(round(val, 0) for val in line.geometry.coords[0]),
                           tuple(round(val, 0) for val in line.geometry.coords[-1]),
                           lineLength)

    else:
        colName = colNameIntersection.pop()
        for line in lines.itertuples():
            lineLength = shapely.length(line.geometry)
            graph.add_edge(tuple(round(val, 0) for val in line.geometry.coords[0]),
                           tuple(round(val, 0) for val in line.geometry.coords[-1]),
                           lineLength / roadClasses[getattr(line, colName)])

    return graph
