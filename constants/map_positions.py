import numpy as np

# ZERO INDEXED => 0 in array is 1 in human language

BOX_ONE_X = 780 + 300
BOX_ONE_Y = 1740 + 300

HORIZONTAL_DISTANCE = 455
VERTICAL_DISTANCE = 392
HALF_HOR = 227

# FROM TOP LEFT:
TO_TOP = np.array([225, -125])
TO_TOP_RIGHT = np.array([455, 0])
TO_BOTTOM_LEFT = np.array([0, 260])
TO_BOTTOM_RIGHT = np.array([455, 260])
TO_BOTTOM = np.array([225, 395])

DISPLACEMENTS = [
    TO_BOTTOM_LEFT // 2,
    np.array([0, 0]),
    TO_TOP // 2,
    TO_TOP,
    (TO_TOP + TO_TOP_RIGHT) // 2,
    TO_TOP_RIGHT,
    (TO_TOP_RIGHT + TO_BOTTOM_RIGHT) // 2,
    TO_BOTTOM_RIGHT,
    (TO_BOTTOM_RIGHT + TO_BOTTOM) // 2,
    TO_BOTTOM,
    (TO_BOTTOM_LEFT + TO_BOTTOM) // 2,
    TO_BOTTOM_LEFT
]

ROTATE_ANGLES = [
    0,
    0,
    120,
    0,
    60,
    0,
    0,
    0,
    120,
    0,
    60,
    0
]

TOP_LEFT_PIXEL = [
    # Lowest row
    (BOX_ONE_X, BOX_ONE_Y),
    (BOX_ONE_X + HORIZONTAL_DISTANCE, BOX_ONE_Y),
    (BOX_ONE_X + 2 * HORIZONTAL_DISTANCE, BOX_ONE_Y),
    (BOX_ONE_X + 3 * HORIZONTAL_DISTANCE, BOX_ONE_Y),
    (BOX_ONE_X + 4 * HORIZONTAL_DISTANCE, BOX_ONE_Y),
    # Second lowest row
    (BOX_ONE_X - HALF_HOR, BOX_ONE_Y - VERTICAL_DISTANCE),
    (BOX_ONE_X - HALF_HOR + HORIZONTAL_DISTANCE, BOX_ONE_Y - VERTICAL_DISTANCE),
    (BOX_ONE_X - HALF_HOR + 2 * HORIZONTAL_DISTANCE, BOX_ONE_Y - VERTICAL_DISTANCE),
    (BOX_ONE_X - HALF_HOR + 3 * HORIZONTAL_DISTANCE, BOX_ONE_Y - VERTICAL_DISTANCE),
    (BOX_ONE_X - HALF_HOR + 4 * HORIZONTAL_DISTANCE, BOX_ONE_Y - VERTICAL_DISTANCE),
    (BOX_ONE_X - HALF_HOR + 5 * HORIZONTAL_DISTANCE, BOX_ONE_Y - VERTICAL_DISTANCE),
    # Middle row
    (BOX_ONE_X - 2 * HALF_HOR, BOX_ONE_Y - 2 * VERTICAL_DISTANCE),
    (BOX_ONE_X - 2 * HALF_HOR + HORIZONTAL_DISTANCE,
     BOX_ONE_Y - 2 * VERTICAL_DISTANCE),
    (BOX_ONE_X - 2 * HALF_HOR + 2 * HORIZONTAL_DISTANCE,
     BOX_ONE_Y - 2 * VERTICAL_DISTANCE),
    (BOX_ONE_X - 2 * HALF_HOR + 3 * HORIZONTAL_DISTANCE,
     BOX_ONE_Y - 2 * VERTICAL_DISTANCE),
    (BOX_ONE_X - 2 * HALF_HOR + 4 * HORIZONTAL_DISTANCE,
     BOX_ONE_Y - 2 * VERTICAL_DISTANCE),
    (BOX_ONE_X - 2 * HALF_HOR + 5 * HORIZONTAL_DISTANCE,
     BOX_ONE_Y - 2 * VERTICAL_DISTANCE),
    (BOX_ONE_X - 2 * HALF_HOR + 6 * HORIZONTAL_DISTANCE,
     BOX_ONE_Y - 2 * VERTICAL_DISTANCE),
    # SECOND ROW
    (BOX_ONE_X - HALF_HOR, BOX_ONE_Y - 3 * VERTICAL_DISTANCE),
    (BOX_ONE_X - HALF_HOR + HORIZONTAL_DISTANCE, BOX_ONE_Y - 3 * VERTICAL_DISTANCE),
    (BOX_ONE_X - HALF_HOR + 2 * HORIZONTAL_DISTANCE,
     BOX_ONE_Y - 3 * VERTICAL_DISTANCE),
    (BOX_ONE_X - HALF_HOR + 3 * HORIZONTAL_DISTANCE,
     BOX_ONE_Y - 3 * VERTICAL_DISTANCE),
    (BOX_ONE_X - HALF_HOR + 4 * HORIZONTAL_DISTANCE,
     BOX_ONE_Y - 3 * VERTICAL_DISTANCE),
    (BOX_ONE_X - HALF_HOR + 5 * HORIZONTAL_DISTANCE,
     BOX_ONE_Y - 3 * VERTICAL_DISTANCE),
    # TOP ROW
    (BOX_ONE_X, BOX_ONE_Y - 4 * VERTICAL_DISTANCE),
    (BOX_ONE_X + HORIZONTAL_DISTANCE, BOX_ONE_Y - 4 * VERTICAL_DISTANCE),
    (BOX_ONE_X + 2 * HORIZONTAL_DISTANCE, BOX_ONE_Y - 4 * VERTICAL_DISTANCE),
    (BOX_ONE_X + 3 * HORIZONTAL_DISTANCE, BOX_ONE_Y - 4 * VERTICAL_DISTANCE),
    (BOX_ONE_X + 4 * HORIZONTAL_DISTANCE, BOX_ONE_Y - 4 * VERTICAL_DISTANCE),
]
