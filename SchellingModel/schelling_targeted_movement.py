"""
Implementation of Schelling model with a few extra ideas
"""

import utility
from simulation_values import max_iterations, neighbour_amount, type_matrix

# value checks
utility.check_values_sanity()
# initialize the graph. -1 is empty
utility.initialize_grid_graph()

# all empty nodes
empty_nodes, empty_map = utility.initialize_empty()

for _ in range(max_iterations):
    corrected_nodes = 0
    for node in utility.iter_positions():
        # empty nodes aren't shuffled around
        if type_matrix[node] == -1:
            continue

        # if the score of this node is too low (it's unstable)
        if utility.neighbourhood_score(node, type_matrix[node]) < \
                neighbour_amount:
            # go through all empty nodes
            for empty in empty_nodes:
                # if the score of this (empty) node is good enough
                if empty_map[empty][type_matrix[node]] >= neighbour_amount:
                    utility.move_node(node, empty, empty_nodes, empty_map)
                    corrected_nodes += 1

                    break
    if corrected_nodes == 0:
        break


# plotting
utility.show_grid()
