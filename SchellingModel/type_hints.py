"""
Just some useful type hints
"""
from typing import List, Tuple, Set, Dict

Colour = Tuple[float, float, float]
Node = Tuple[int, int]
LFloat = List[float]
LInt = List[int]
LColour = List[Colour]
SNode = Set[Node]
EMap = Dict[Node, Dict[int, float]]
