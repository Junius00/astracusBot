import math
import numpy as np

MAP_QLIM = 3
MAP_RLIM = 2
MAP_SLIM = 3

#unit (x, y) vectors in q, r, s directions
VECT_Q = np.array([math.cos(math.pi/3), -math.sin(math.pi/3)])
VECT_R = np.array([0, 1])
VECT_S = np.array([-math.cos(math.pi/3), -math.sin(math.pi/3)])

MAP_ROT = 60
MAP_E_OFFSET = 30
MAP_V_OFFSET = 0

#sorted in 30 degree increments from 0
MAP_EQ_OFFSETS = [
    [(0, -1, 1, 120), (1, -1, 0, 240)],
    [(1, -1, 0, 180)],
    [(1, -1, 0, 120), (1, 0, -1, 240)],
    [(1, 0, -1, 180)],
    [(1, 0, -1, 120), (0, 1, -1, 240)],
    [(0, 1, -1, 180)],
    [(0, 1, -1, 120), (-1, 1, 0, 240)],
    [(-1, 1, 0, 180)],
    [(-1, 1, 0, 120), (-1, 0, 1, 240)],
    [(-1, 0, 1, 180)],
    [(-1, 0, 1, 120), (0, -1, 1, 240)],
    [(0, -1, 1, 180)]
]