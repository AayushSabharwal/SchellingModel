"""
Implementation of Schelling model
"""
import simulation_parameters as params
import utility


# value checks
utility.check_values_sanity()
# initialize the graph. -1 is empty
utility.initialize_grid_graph()

params.empty_nodes = {node for node in utility.iter_positions() if params.type_matrix[node] == -1}
params.tactic = params.tactic()

params.grid_history.append(params.type_matrix.copy())
for _ in range(params.max_iterations):
    corrected_nodes = 0
    nodes_to_move = []  # elements should be tuples of the form (from: Node, to: Node)
    for node in utility.iter_positions():
        # empty nodes aren't shuffled around
        if params.type_matrix[node] == -1:
            continue

        # if the score of this node is too low (it's unstable) and there actually are nodes we can
        # move to
        if utility.neighbourhood_score(node, params.type_matrix[node]) < \
                params.neighbour_amount and len(params.empty_nodes) > 0:
            target = params.tactic.handle_empty_node(node)
            if target is not None:
                nodes_to_move.append((node, target))
                corrected_nodes += 1

    # actually carry out the movement
    for movement in nodes_to_move:
        params.tactic.move_node(movement[0], movement[1])

    params.grid_history.append(params.type_matrix.copy())
    if corrected_nodes == 0:
        grid_history = params.grid_history.pop()
        break


# plotting
utility.show_grid()
