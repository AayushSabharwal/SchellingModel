from enum import Enum
from type_hints import GridXY


class InfectionState(Enum):
    """
    Enum to represent possible states of an agent
    """
    SUS = 1  # susceptible
    INF = 2  # infected
    REC = 3  # recovered (immune)


def sqr_euler_distance(a: GridXY, b: GridXY):
    """
    Function to get square of euler distance between two grid points
    """
    return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])
