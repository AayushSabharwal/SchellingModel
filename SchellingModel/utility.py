import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from type_hints import Node
import simulation_parameters as params


# generator function to iterate through all positions on the grid
def iter_positions():
    for i in range(params.side):
        for j in range(params.side):
            yield (i, j)


# just checking if the inputted values are valid
def check_values_sanity():
    assert params.empty_fraction < 1.  # fraction of empty cells should be < 1
    assert params.gets_along_with.shape[0] == params.gets_along_with.shape[1]  # square matrix
    assert len(params.types_distribution) == len(params.type_colours) \
        == params.gets_along_with.shape[0]  # consistency check
    # all values should be in [-1, 1]
    assert all(abs(x) <= 1 for x in np.nditer(params.gets_along_with))
    assert sum(params.types_distribution) == 1.    # sum of fractions is 1


# check if a grid index is valid
def valid_node(node: Node):
    return node[0] >= 0 and node[0] < params.side and node[1] >= 0 and node[1] < params.side


# get the neighbourhood_score of a cell
def neighbourhood_score(node: Node, looking_for_type: int):
    value = 0
    nneighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            # index of the neighbour
            neighbour = tuple(np.add(node, (i, j)))
            # if the node is a valid node, it isn't the central node, and is not empty
            if valid_node(neighbour) and (i, j) != (0, 0) and params.type_matrix[neighbour] != -1:
                nneighbours += 1
                value += params.gets_along_with[looking_for_type, params.type_matrix[neighbour]]
    # if prevents division by 0
    return value / nneighbours if nneighbours != 0 else 0


# initialze the grid
def initialize_grid_graph():
    all_positions = list(iter_positions())
    # randomly choose empty nodes

    _empty_nodes = random.sample(all_positions,
                                 int(params.side * params.side * params.empty_fraction))
    # set empty nodes type
    for node in _empty_nodes:
        params.type_matrix[node] = -1

    # number of non-empty nodes
    typeable_nodes = params.side * params.side - len(_empty_nodes)
    # set of nodes available to assign to a type
    available_nodes = set(all_positions).difference(_empty_nodes)
    for i in range(params.types - 1):
        # randomly choose the requisite number of nodes
        type_nodes = random.sample(available_nodes, int(
            typeable_nodes * params.types_distribution[i]))
        # assign the type
        for node in type_nodes:
            params.type_matrix[node] = i
        # remove the used nodes from the set of nodes available to assign to other types
        available_nodes = available_nodes.difference(type_nodes)

    # last type isn't in the for loop so all the rest get assigned
    for node in available_nodes:
        params.type_matrix[node] = params.types - 1


# initialize the empty_map variable
def initialize_empty_map():
    params.empty_map = {enode: {i: neighbourhood_score(enode, i)
                                for i in range(params.types)} for enode in params.empty_nodes}
    return params.empty_map


# display the grid
def show_grid():
    colour_map = get_colour_map(params.type_matrix)
    fig, ax = plt.subplots()
    ax.imshow(colour_map)
    ax.set_xticks(np.arange(0, params.side, 1))
    ax.set_yticks(np.arange(0, params.side, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    axstage = plt.axes([0.2, 0.05, 0.65, 0.03])
    sslider = Slider(axstage, 'Stage', 0, len(params.grid_history) - 1,
                     valinit=len(params.grid_history) - 1, valstep=1)

    def update(val):
        val = int(val)
        colour_map = get_colour_map(params.grid_history[val])
        ax.imshow(colour_map)

    sslider.on_changed(update)
    plt.show()


# generates a colour map for plotting
def get_colour_map(grid: np.ndarray):
    colour_map = np.ndarray((params.side, params.side, 3), dtype=float)
    for i in range(params.side):
        for j in range(params.side):
            if grid[(i, j)] == -1:
                colour_map[(i, j)] = params.empty_colour
            else:
                colour_map[(i, j)] = params.type_colours[grid[(i, j)]]
    return colour_map
