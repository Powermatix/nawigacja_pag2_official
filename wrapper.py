from a_graph import make_dict
# in the finished version: choose to import from a_star or a_star_vis
# a_star: no plotting
# a_star_vis: slower version with plotting for testing/demos
# set PLOT, PLOT_EXT, PRINT directly in a_star_vis.py
from a_star_vis import astar

nodes, edges = make_dict('a_demo.shp')
#print(astar('353754.0_534559.0','353637.0_534495.0',nodes,edges))
print(astar('353754.0_534559.0','354929.0_533759.0',nodes,edges))
# print(nodes)
# print(edges)
