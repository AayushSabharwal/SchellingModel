"""
Implementation of Schelling model with a few extra ideas
"""

import numpy as np
from matplotlib import pyplot as plt
import utility_functions as utility

side = 50   # number of side in grid
empty_fraction = 0.3    # fraction of empty cells
types_distribution = [0.33, 0.33, 0.34]  # distribution of each type
type_colours = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]   # colour of each type
gets_along_with = {0: [0, 1], 1: [1], 2: [2]}
empty_colour = (0.2, 0.2, 0.2)    # colour of empty nodes
iterations = 20
neighbour_fraction = 0.75

# value checks
assert empty_fraction < 1.
assert len(types_distribution) == len(type_colours)
assert sum(types_distribution) == 1.

type_matrix = np.zeros((side, side), dtype=int)
# initialize the graph. -1 is empty
utility.initialize_grid_graph(type_matrix, side, empty_fraction, types_distribution)

position_map = {(x, y): (y, -x) for x, y in utility.iter_positions(side)}
empty_nodes = {(x, y) for x, y in utility.iter_positions(side)
               if type_matrix[(x, y)] == -1}

for _ in range(iterations):
    corrected_nodes = 0
    for node in utility.iter_positions(side):
        if type_matrix[node] == -1:
            continue

        if utility.neighbourhood_value(node, type_matrix, gets_along_with, type_matrix[node]) < \
                neighbour_fraction:
            for empty in empty_nodes:
                if utility.neighbourhood_value(empty, type_matrix, gets_along_with,
                                               type_matrix[node]) \
                        >= neighbour_fraction:
                    type_matrix[empty] = type_matrix[node]
                    type_matrix[node] = -1
                    empty_nodes.remove(empty)
                    empty_nodes.add(node)
                    corrected_nodes += 1
                    break
    if corrected_nodes == 0:
        break


colour_map = utility.get_colour_map(side, type_matrix, type_colours, empty_colour)

fig, ax = plt.subplots()
ax.imshow(colour_map)
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0)
ax.set_xticks(np.arange(0, side, 1))
ax.set_yticks(np.arange(0, side, 1))
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.show()
