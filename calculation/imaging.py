import math
import numpy as np
from calculation.grid import is_edge
from constants.map.axes import VECT_Q, VECT_R, VECT_S

from constants.map.positions import CENTER_HEX, HEX_DIAMETER, HEX_RADIUS_EDGE, HEX_RADIUS_VERTEX

def get_unit_vector(angle):
    angle = (angle + 90) % 360
    angle *= math.pi/180
    return np.array([math.cos(angle), -math.sin(angle)])

def c_to_xy(c):
    q, _, s, a = c
    a_mag = HEX_RADIUS_EDGE if is_edge(c) else HEX_RADIUS_VERTEX
    x, y = CENTER_HEX + (q * VECT_Q + s * VECT_S) * HEX_DIAMETER + get_unit_vector(a) * a_mag

    return int(x), int(y)
