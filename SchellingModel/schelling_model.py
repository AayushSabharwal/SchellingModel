"""
Implementation of Schelling model
"""
import simulation_parameters as params
import movement_tactics as tactics
import utility


# value checks
utility.check_values_sanity()
# initialize the graph. -1 is empty
utility.initialize_grid_graph()

params.empty_nodes = {node for node in utility.iter_positions() if params.type_matrix[node] == -1}
# print(params.empty_nodes)
params.tactic = tactics.TargetedMovement()

params.grid_history.append(params.type_matrix.copy())
for _ in range(params.max_iterations):
    corrected_nodes = 0
    for node in utility.iter_positions():
        # empty nodes aren't shuffled around
        if params.type_matrix[node] == -1:
            continue

        # if the score of this node is too low (it's unstable)
        if utility.neighbourhood_score(node, params.type_matrix[node]) < \
                params.neighbour_amount:
            corrected_nodes += params.tactic.handle_empty_node(node)

    params.grid_history.append(params.type_matrix.copy())
    if corrected_nodes == 0:
        grid_history = params.grid_history.pop()
        break


# plotting
utility.show_grid()
