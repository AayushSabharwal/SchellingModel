from enum import Enum
from type_hints import GridXY


class InfectionState(Enum):
    SUS = 1
    INF = 2
    REC = 3


def sqr_euler_distance(a: GridXY, b: GridXY):
    return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])
