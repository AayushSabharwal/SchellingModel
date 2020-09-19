import random
from typing import List, Tuple, Dict
import numpy as np

# type hints
LFloat = List[float]
LInt = List[int]
DIntLInt = Dict[int, LInt]
Colour = Tuple[float, float, float]
Node = Tuple[int, int]
LColour = List[Colour]


# generator function to iterate through all positions on the grid
def iter_positions(side: int):
    for i in range(side):
        for j in range(side):
            yield (i, j)


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
