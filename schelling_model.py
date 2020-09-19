"""
Implementation of Schelling model with a few extra ideas
"""

import numpy as np
from matplotlib import pyplot as plt
import utility_functions as utility

side = 50   # size of grid
empty_fraction = 0.3    # fraction of empty cells
types_distribution = [0.33, 0.33, 0.34]  # distribution of each type, among non-empty cells
type_colours = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]   # colour of each type of cell
# adjacency matrix. Denotes how well (or not well) two types get along
# Values between -1 and 1
# 0 doesn't affect the neighbourhood_value
# Ideally, keep the diagonal 1 (everyone gets along with the same type)
gets_along_with = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])
empty_colour = (0.2, 0.2, 0.2)    # colour of empty cells
max_iterations = 10  # maximum iterations the simulation will run for
neighbour_amount = 0.75  # what threshold of neighbourhood_score is stable?

# value checks
assert empty_fraction < 1.  # fraction of empty cells should be < 1
assert gets_along_with.shape[0] == gets_along_with.shape[1]  # square matrix
assert len(types_distribution) == len(type_colours) == gets_along_with.shape[0]  # consistency check
assert all(abs(x) <= 1 for x in np.nditer(gets_along_with))  # all values should be in [-1, 1]
assert sum(types_distribution) == 1.    # sum of fractions is 1

type_matrix = np.zeros((side, side), dtype=int)  # type of (i, j) node
# initialize the graph. -1 is empty
utility.initialize_grid_graph(type_matrix, side, empty_fraction, types_distribution)
# all empty nodes
empty_nodes = {(x, y) for x, y in utility.iter_positions(side) if type_matrix[(x, y)] == -1}

for _ in range(max_iterations):
    corrected_nodes = 0
    for node in utility.iter_positions(side):
        # empty nodes aren't shuffled around
        if type_matrix[node] == -1:
            continue

        # if the score of this node is too low (it's unstable)
        if utility.neighbourhood_score(node, type_matrix, gets_along_with, type_matrix[node]) < \
                neighbour_amount:
            # go through all empty nodes
            for empty in empty_nodes:
                # if the score of this node is good enough
                if utility.neighbourhood_score(empty, type_matrix, gets_along_with,
                                               type_matrix[node]) \
                        >= neighbour_amount:
                    type_matrix[empty] = type_matrix[node]
                    type_matrix[node] = -1
                    empty_nodes.remove(empty)
                    empty_nodes.add(node)
                    corrected_nodes += 1
                    break
    if corrected_nodes == 0:
        break


# plotting
colour_map = utility.get_colour_map(side, type_matrix, type_colours, empty_colour)
position_map = {(x, y): (y, -x) for x, y in utility.iter_positions(side)}

fig, ax = plt.subplots()
ax.imshow(colour_map)
ax.set_xticks(np.arange(0, side, 1))
ax.set_yticks(np.arange(0, side, 1))
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.show()
