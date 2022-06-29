import json
import os
import cv2
import numpy as np
from scipy import ndimage
from constants.storage import FOLDER_DATA, FOLDER_ASSETS
from constants.map_positions import TOP_LEFT_PIXEL, DISPLACEMENTS, ROTATE_ANGLES

"""
1. Reset map function
2. Add item function (Colour, type, Box number, position)
3. Remove item function (Box number, position)
4. Load JSON from storage
5. Export to storage
6. Generate image (Array)

LEFT, TOP LEFT, TOP RIGHT, RIGHT, BOTTOM RIGHT, BOTTOM LEFT.
"""


class Map():
    def __init__(self):
        self.filename = os.path.join(FOLDER_DATA, "Map.json")
        self.map_img = os.path.join(FOLDER_ASSETS, "board.png")
        self.map = self.load_from_json()

    def reset_map(self):
        self.map = [["", "", "", "", "", "", "", "", "", "", "", ""]
                    for _ in range(29)]

    def add_item(self, colour, type, box, position):
        self.map[box - 1, position - 1] = colour + type

    def remove_item(self, box, position):
        self.map[box - 1, position - 1] = ""

    def load_from_json(self):
        if os.path.exists(self.filename):
            f = open(self.filename, 'r')
            res = json.load(f)
            f.close()

            return res

        return [["blackdoor", "blackflag", "blackdoor", "blackflag", "blackdoor", "blackbanner", "blackdoor", "blackbanner", "blackdoor", "blackbanner", "blackdoor", "blackbanner"] for _ in range(29)]

    def save_to_json(self):
        with open(self.filename, 'w') as f:
            json.dump(self.items, f)

    def generate_map(self):
        empty_board = cv2.imread(self.map_img)
        empty_board = cv2.copyMakeBorder(
            empty_board, 300, 300, 300, 300, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        for box in range(29):
            for position in range(12):
                if self.map[box][position] != "":
                    image = cv2.imread(os.path.join(
                        FOLDER_ASSETS, self.map[box][position] + '.png'), cv2.IMREAD_UNCHANGED)
                    image = ndimage.rotate(image, ROTATE_ANGLES[position])
                    shape = image.shape
                    to_center = np.array(shape) // 2
                    X = TOP_LEFT_PIXEL[box][0] + \
                        DISPLACEMENTS[position][0] - to_center[1]
                    Y = TOP_LEFT_PIXEL[box][1] + \
                        DISPLACEMENTS[position][1] - to_center[0]
                    # addition = cv2.addWeighted(
                    #     empty_board[Y:Y + shape[0], X:X + shape[1]], 0.5, image, 0.7, 0)
                    # empty_board[Y:Y + shape[0], X:X + shape[1]] = addition
                    self.add_transparent_image(empty_board, image, X, Y)

        h, w = empty_board.shape[:2]
        nw = 1000
        w, h = nw, int(h * nw/w)
        empty_board = cv2.resize(empty_board, (w, h))
        cv2.imshow("M", empty_board)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def add_transparent_image(self, background, foreground, x_offset=None, y_offset=None):
        bg_h, bg_w, bg_channels = background.shape
        fg_h, fg_w, fg_channels = foreground.shape

        assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
        assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'

        # center by default
        if x_offset is None:
            x_offset = (bg_w - fg_w) // 2
        if y_offset is None:
            y_offset = (bg_h - fg_h) // 2

        w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
        h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

        if w < 1 or h < 1:
            return

        # clip foreground and background images to the overlapping regions
        bg_x = max(0, x_offset)
        bg_y = max(0, y_offset)
        fg_x = max(0, x_offset * -1)
        fg_y = max(0, y_offset * -1)
        foreground = foreground[fg_y:fg_y + h, fg_x:fg_x + w]
        background_subsection = background[bg_y:bg_y + h, bg_x:bg_x + w]

        # separate alpha and color channels from the foreground image
        foreground_colors = foreground[:, :, :3]
        alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

        # construct an alpha_mask that matches the image shape
        alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

        # combine the background with the overlay image weighted by alpha
        composite = background_subsection * \
            (1 - alpha_mask) + foreground_colors * alpha_mask

        # overwrite the section of the background image that has been updated
        background[bg_y:bg_y + h, bg_x:bg_x + w] = composite