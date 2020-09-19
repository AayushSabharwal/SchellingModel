"""
Implementation of Schelling model with a few extra ideas
"""
from matplotlib import pyplot as plt
import numpy as np
from utility_functions import *

side = 30   # number of side in grid
empty_fraction = 0.3    # fraction of empty cells
types_distribution = [0.33, 0.33, 0.34]  # distribution of each type
type_colours = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]   # colour of each type
empty_colour = (0.2, 0.2, 0.2)    # colour of empty nodes
iterations = 60
neighbour_fraction = 0.5

# value checks
assert empty_fraction < 1.
assert len(types_distribution) == len(type_colours)
assert sum(types_distribution) == 1.

type_matrix = np.zeros((side, side), dtype=int)
# initialize the graph. -1 is empty
initialize_grid_graph(type_matrix, side, empty_fraction, tyninpes_distribution)

position_map = {(x, y): (y, -x) for x, y in iter_positions(side)}
empty_nodes = set([(x, y)
                   for x, y in g.keys() if type_matrix[(x, y)] == -1])
print(len(empty_nodes))
for _ in range(iterations):
    for node in g.keys():
        nvalue = len([n for n in g[node] if type_matrix[node]
                      in [type_matrix[n], -1]])/len(g[node])
        if nvalue < neighbour_fraction:
            for empty in empty_nodes:
                envalue = len([n for n in g[empty] if type_matrix[node] in [
                              type_matrix[n], -1]])/len(g[node])
                if envalue >= neighbour_fraction:
                    empty_nodes.add(node)
                    empty_nodes.remove(empty)
                    type_matrix[empty] = type_matrix[node]
                    type_matrix[node] = -1
                    break

colour_map = get_colour_map(side, type_matrix, type_colours, empty_colour)

fig, ax = plt.subplots()
ax.imshow(colour_map)
# ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0)
ax.set_xticks(np.arange(0, side, 1))
ax.set_yticks(np.arange(0, side, 1))
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.show()
