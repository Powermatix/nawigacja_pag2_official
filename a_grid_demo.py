# set PLOT and PLOT_EXT to True directly in a_star_vis.py (default)
from a_star_vis import astar
from a_grid import generate_cartesian

nodes, edges = generate_cartesian(1,1,6,6)
print(astar("1_1","6_6",nodes,edges))
