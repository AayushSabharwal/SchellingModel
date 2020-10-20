from enum import Enum
from type_hints import GridXY
import simulation_parameters as params


class InfectionState(Enum):
    """
    Enum to represent possible states of an agent
    """
    SUS = 1  # susceptible
    INF = 2  # infected
    REC = 3  # recovered (immune)
    VAC = 4  # vaccinated (also immune)


def sqr_toroidal_distance(a: GridXY, b: GridXY):
    """
    Function to get square of toroidal distance between two grid points

    Parameters
    ----------
    a, b : GridXY
        points between which sqr toroidal distance should be calculated

    Returns
    -------
    float
        the toroidal distance between a and b
    """
    xdelta = abs(a[0] - b[0])
    if xdelta > params.params['grid_width'] / 2:
        xdelta = params.params['grid_width'] / 2 - xdelta

    ydelta = abs(a[1] - b[1])
    if ydelta > params.params['grid_height'] / 2:
        ydelta = params.params['grid_height'] / 2 - ydelta
    return xdelta**2 + ydelta**2


def toroidal_distance(a: GridXY, b: GridXY):
    """
    Function to get toroidal distance between two grid points

    Parameters
    ----------
    a, b : GridXY
        points between which toroidal distance should be calculated

    Returns
    -------
    float
        the toroidal distance between a and b
    """
    return sqr_toroidal_distance(a, b) ** 0.5
