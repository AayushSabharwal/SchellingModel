import numpy as np
import random
from typing import List, Tuple, Dict

LFloat = List[float]
Colour = Tuple[float, float, float]
LColour = List[Colour]


def iter_positions(side: int):
    for i in range(side):
        for j in range(side):
            yield (i, j)


def position_to_index(x: int, y: int, side: int):
    return x * side + y


def initialize_grid_graph(type_matrix: np.ndarray, side: int, empty_fraction: float,
                          types_distribution: LFloat):
    empty_nodes = random.sample(
        list(g.keys()), int(side * side * empty_fraction))

    for node in empty_nodes:
        type_matrix[node] = -1

    typeable_nodes = side * side - len(empty_nodes)
    available_nodes = set(g.keys()).difference(empty_nodes)
    for i in range(types - 1):
        type_nodes = random.sample(available_nodes, int(
            typeable_nodes * types_distribution[i]))
        for node in type_nodes:
            type_matrix[node] = i
        available_nodes = available_nodes.difference(type_nodes)
    for node in available_nodes:
        type_matrix[node] = types - 1


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
