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
        Returns the empty node this node will be moved to

        The empty node moved to should be removed from params.empty_nodes
        """

    def move_node(self, node: Node, empty: Node):
        """
        Moves node to empty
        """
        params.type_matrix[empty] = params.type_matrix[node]
        params.type_matrix[node] = -1
        params.empty_nodes.add(node)


class RandomMovement(MovementTactic):
    """
    Moves unstable node to random empty node

    This is the default tactic of Schelling model
    """

    def handle_empty_node(self, node: Node):
        if len(params.empty_nodes) == 0:
            return None

        target = random.choice(tuple(params.empty_nodes))
        params.empty_nodes.remove(target)
        return target


class TargetedMovement(MovementTactic):
    def __init__(self):
        self.empty_map = utility.initialize_empty_map()

    def handle_empty_node(self, node: Node):
        target = None
        for empty in params.empty_nodes:
            # if the score of this (empty) node is good enough
            if self.empty_map[empty][params.type_matrix[node]] >= params.neighbour_amount:
                target = empty
                break
        if target is not None:
            params.empty_nodes.remove(target)
        return target

    # move a node to target (empty) node
    def move_node(self, node: Node, empty: Node):
        super().move_node(node, empty)  # super allows calling base class method
        self.empty_map.pop(empty)

        # after moving, affected neighbour cells of moved cells have to be updated
        self.update_neighbours(node)
        self.update_neighbours(empty)

    def update_neighbours(self, node: Node):
        for i in range(-1, 2):
            for j in range(-1, 2):
                # index of the neighbour
                neighbour = tuple(np.add(node, (i, j)))
                # if the node is a valid node, it isn't the central node, and is not empty
                if utility.valid_node(neighbour) and params.type_matrix[neighbour] == -1:
                    self.empty_map[neighbour] = {i: utility.neighbourhood_score(neighbour, i)
                                                 for i in range(params.types)}
