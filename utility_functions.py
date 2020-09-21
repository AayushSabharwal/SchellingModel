import random
from typing import List, Tuple, Set, Dict
import numpy as np
from matplotlib import pyplot as plt

# type hints
Colour = Tuple[float, float, float]
Node = Tuple[int, int]
LFloat = List[float]
LInt = List[int]
LColour = List[Colour]
SNode = Set[Node]
EMap = Dict[Node, Dict[int, float]]


# generator function to iterate through all positions on the grid
def iter_positions(side: int):
    for i in range(side):
        for j in range(side):
            yield (i, j)


# just checking if the inputted values are valid
def check_values_sanity(empty_fraction: float, gets_along_with: np.matrix,
                        types_distribution: LFloat, type_colours: LColour):
    assert empty_fraction < 1.  # fraction of empty cells should be < 1
    assert gets_along_with.shape[0] == gets_along_with.shape[1]  # square matrix
    assert len(types_distribution) == len(
        type_colours) == gets_along_with.shape[0]  # consistency check
    assert all(abs(x) <= 1 for x in np.nditer(gets_along_with))  # all values should be in [-1, 1]
    assert sum(types_distribution) == 1.    # sum of fractions is 1


# check if a grid index is valid
def valid_node(node: Node, side: int):
    return node[0] >= 0 and node[0] < side and node[1] >= 0 and node[1] < side


# get the neighbourhood_score of a cell
def neighbourhood_score(node: Node, type_matrix: np.ndarray, gets_along_with: np.matrix,
                        looking_for_type: int):
    side = type_matrix.shape[0]
    value = 0
    nneighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            # index of the neighbour
            neighbour = tuple(np.add(node, (i, j)))
            # if the node is a valid node, it isn't the central node, and is not empty
            if valid_node(neighbour, side) and (i, j) != (0, 0) and type_matrix[neighbour] != -1:
                nneighbours += 1
                value += gets_along_with[looking_for_type, type_matrix[neighbour]]
    # if prevents division by 0
    return value / nneighbours if nneighbours != 0 else 0


# initialze the grid
def initialize_grid_graph(type_matrix: np.ndarray, side: int, empty_fraction: float,
                          types_distribution: LFloat):
    all_positions = list(iter_positions(side))
    # randomly choose empty nodes
    empty_nodes = random.sample(all_positions,
                                int(side * side * empty_fraction))
    # set empty nodes type
    for node in empty_nodes:
        type_matrix[node] = -1

    types = len(types_distribution)
    # number of non-empty nodes
    typeable_nodes = side * side - len(empty_nodes)
    # set of nodes available to assign to a type
    available_nodes = set(all_positions).difference(empty_nodes)
    for i in range(types - 1):
        # randomly choose the requisite number of nodes
        type_nodes = random.sample(available_nodes, int(
            typeable_nodes * types_distribution[i]))
        # assign the type
        for node in type_nodes:
            type_matrix[node] = i
        # remove the used nodes from the set of nodes available to assign to other types
        available_nodes = available_nodes.difference(type_nodes)

    # last type isn't in the for loop so all the rest get assigned
    for node in available_nodes:
        type_matrix[node] = types - 1


def initialize_empty(side: int, type_matrix: np.ndarray, gets_along_with: np.matrix, types: int):
    empty_nodes = {node for node in iter_positions(side) if type_matrix[node] == -1}
    empty_map = {enode: {i: neighbourhood_score(enode, type_matrix, gets_along_with, i)
                         for i in range(types)} for enode in empty_nodes}

    return empty_nodes, empty_map


def move_node(node: Node, empty: Node, side: int, types: int, type_matrix: np.ndarray,
              gets_along_with: np.matrix, empty_nodes: SNode, empty_map: EMap):
    type_matrix[empty] = type_matrix[node]
    type_matrix[node] = -1
    empty_nodes.remove(empty)
    empty_nodes.add(node)
    empty_map.pop(empty)

    for i in range(-1, 2):
        for j in range(-1, 2):
            # index of the neighbour
            neighbour = tuple(np.add(node, (i, j)))
            # if the node is a valid node, it isn't the central node, and is not empty
            if valid_node(neighbour, side) and type_matrix[neighbour] == -1:
                empty_map[neighbour] = {i: neighbourhood_score(neighbour, type_matrix,
                                                               gets_along_with, i)
                                        for i in range(types)}


# display the grid
def show_grid(side: int, type_matrix: np.ndarray, type_colours: LColour, empty_colour: Colour):
    colour_map = get_colour_map(side, type_matrix, type_colours, empty_colour)
    fig, ax = plt.subplots()
    ax.imshow(colour_map)
    ax.set_xticks(np.arange(0, side, 1))
    ax.set_yticks(np.arange(0, side, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.show()


# generates a colour map for plotting
def get_colour_map(side: int, type_matrix: np.ndarray, type_colours: LColour,
                   empty_colour: Colour):
    colour_map = np.ndarray((side, side, 3), dtype=float)
    for i in range(side):
        for j in range(side):
            if type_matrix[(i, j)] == -1:
                colour_map[(i, j)] = empty_colour
            else:
                colour_map[(i, j)] = type_colours[type_matrix[(i, j)]]
    return colour_map
