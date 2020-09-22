"""
Handles targeted movement. Unstable nodes are moved to the first node found where it is stable
"""
from abc import ABC, abstractmethod
import random
import numpy as np
from type_hints import Node
import simulation_parameters as params
import utility


class MovementTactic(ABC):
    """
    Abstract base class for all movement movement_tactics

    Every movement tactic must handle how a node moves when it is unstable, hence it must implement
    the handle_empty_node method
    """
    @abstractmethod
    def handle_empty_node(self, node: Node) -> int:
        """
        Moves the empty nodes

        Returns 1 if node is moved, 0 if it isn't
        """


class RandomMovement(MovementTactic):
    """
    Moves unstable node to random empty node

    This is the default tactic of Schelling model
    """

    def handle_empty_node(self, node: Node):
        chosen = random.choice(tuple(params.empty_nodes))
        params.type_matrix[chosen] = params.type_matrix[node]
        params.type_matrix[node] = -1
        params.empty_nodes.remove(chosen)
        params.empty_nodes.add(node)
        return 1


class TargetedMovement(MovementTactic):
    def __init__(self):
        self.empty_map = utility.initialize_empty_map()

    def handle_empty_node(self, node: Node):
        for empty in params.empty_nodes:
            # if the score of this (empty) node is good enough
            if self.empty_map[empty][params.type_matrix[node]] >= params.neighbour_amount:
                self.move_node(node, empty)
                return 1
        return 0

    # move a node to target (empty) node
    def move_node(self, node: Node, empty: Node):
        params.type_matrix[empty] = params.type_matrix[node]
        params.type_matrix[node] = -1
        params.empty_nodes.remove(empty)
        params.empty_nodes.add(node)
        self.empty_map.pop(empty)

        # after moving, affected neighbour cells of moved cells have to be updated
        self.update_neighbouts(node)
        self.update_neighbouts(empty)

    def update_neighbouts(self, node: Node):
        for i in range(-1, 2):
            for j in range(-1, 2):
                # index of the neighbour
                neighbour = tuple(np.add(node, (i, j)))
                # if the node is a valid node, it isn't the central node, and is not empty
                if utility.valid_node(neighbour) and params.type_matrix[neighbour] == -1:
                    self.empty_map[neighbour] = {i: utility.neighbourhood_score(neighbour, i)
                                                 for i in range(params.types)}
