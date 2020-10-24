from enum import Enum
from typing import Tuple


class InfectionState(Enum):
    """
    Enum to represent possible states of an agent
    """
    SUS = 1  # susceptible
    INF = 2  # infected
    REC = 3  # recovered (immune)
    VAC = 4  # vaccinated (also immune)


def sqr_toroidal_distance(a: Tuple[int, int], b: Tuple[int, int], grid_width: int, grid_height: int):
    """
    Function to get square of toroidal distance between two grid points

    Parameters
    ----------
    a, b : GridXY
        Points between which sqr toroidal distance should be calculated
    grid_width, grid_height: int
        Grid dimensions

    Returns
    -------
    float
        Square of toroidal distance between a and b
    """
    xdelta = abs(a[0] - b[0])
    if xdelta > grid_width / 2:
        xdelta = grid_width / 2 - xdelta

    ydelta = abs(a[1] - b[1])
    if ydelta > grid_height / 2:
        ydelta = grid_height / 2 - ydelta
    return xdelta**2 + ydelta**2


def toroidal_distance(a: Tuple[int, int], b: Tuple[int, int], grid_width: int, grid_height: int):
    """
    Function to get toroidal distance between two grid points

    Parameters
    ----------
    a, b : Tuple[int, int]
        Points between which toroidal distance should be calculated
    grid_width, grid_height: int
        Grid dimensions
    Returns
    -------
    float
        Toroidal distance between a and b
    """
    return sqr_toroidal_distance(a, b, grid_width, grid_height) ** 0.5
