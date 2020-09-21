"""
Implementation of Schelling model with a few extra ideas
"""

import numpy as np
import utility_functions as utility

side = 70   # size of grid
empty_fraction = 0.2    # fraction of empty cells
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
max_iterations = 100  # maximum iterations the simulation will run for
neighbour_amount = 0.75  # what threshold of neighbourhood_score is stable?

# value checks
utility.check_values_sanity(empty_fraction, gets_along_with, types_distribution, type_colours)
types = len(types_distribution)

type_matrix = np.zeros((side, side), dtype=int)  # type of (i, j) node
# initialize the graph. -1 is empty
utility.initialize_grid_graph(type_matrix, side, empty_fraction, types_distribution)
# all empty nodes
empty_nodes, empty_map = utility.initialize_empty(side, type_matrix, gets_along_with, types)

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
                # if the score of this (empty) node is good enough
                if empty_map[empty][type_matrix[node]] >= neighbour_amount:
                    utility.move_node(node, empty, side, types, type_matrix, gets_along_with,
                                      empty_nodes, empty_map)
                    corrected_nodes += 1

                    break
    if corrected_nodes == 0:
        break


# plotting
utility.show_grid(side, type_matrix, type_colours, empty_colour)
