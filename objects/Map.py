from ast import literal_eval
import json
import os
from re import L
import cv2
import numpy as np
from scipy import ndimage
from calculation.buildings import can_build_house
from calculation.grid import check_equivalent, find_equivalent, find_neighbours
from calculation.imaging import c_to_xy
from constants.map.assets import MAP_ASSET_FILENAMES
from constants.map.drawing import CHOICE_COLOR, CHOICE_FONT, CHOICE_FONTSCALE, CHOICE_RADIUS, CHOICE_THICKNESS
from constants.map.positions import BORDER_SIZE
from constants.names import B_HOUSE, B_ROAD, B_VILLAGE, KEY_B
from constants.storage import FOLDER_DATA, FOLDER_ASSETS
from objects.Building import Building

"""
1. Reset map function
2. Add item function (Colour, type, Box number, position)
3. Remove item function (Box number, position)
4. Load JSON from storage
5. Export to storage
6. Generate image (Array)
"""


class Map():
    def __init__(self):
        self.filename = os.path.join(FOLDER_DATA, "map.json")
        self.map_img = os.path.join(FOLDER_ASSETS, "board.png")
        self.current_map_img = os.path.join(FOLDER_ASSETS, "current_board.png")
        self.load_from_json()

    def reset_map(self):
        self.map = {}

    def place_building(self, c, building):
        self.map[c] = building
        building.c = c

    def remove_building(self, c):
        if c in self.map:
            del self.map[c]

    def get_building(self, c):
        if c in self.map:
            return self.map[c]
        
        possible = find_equivalent(c)
        ret = None

        for p in possible:
            ret = self.map.get(p, None)
            if ret:
                break
        
        return ret
    
    def load_from_json(self):
        if os.path.exists(self.filename):
            f = open(self.filename, 'r')
            res = json.load(f)
            f.close()
            
            res = {literal_eval(k): Building().to_obj(v) for k, v in res.items()}
            self.map = res

            return

        self.reset_map()

    def save_to_json(self):
        map_obj = {str(k): v.to_obj() for k, v in self.map.items()}
        with open(self.filename, 'w') as f:
            json.dump(map_obj, f)

    def generate_map_img(self, choices=None):
        board = cv2.imread(self.map_img)
        board = cv2.copyMakeBorder(
            board, 
            *[BORDER_SIZE for _ in range(4)], 
            cv2.BORDER_CONSTANT, value=[255, 255, 255])

        for c, building in self.map.items():
            image = cv2.imread(os.path.join(
                        FOLDER_ASSETS, MAP_ASSET_FILENAMES[building.owner][building.name]), cv2.IMREAD_UNCHANGED)
                
            if building.name == B_ROAD:
                image = ndimage.rotate(image, 90 - c[3])

            yadj, xadj = (np.array(image.shape) // 2)[:2]
            x, y = c_to_xy(c)
            x, y = x - xadj, y - yadj

            self.add_transparent_image(board, image, x, y)

        if choices:
            for i, c in enumerate(choices):
                x, y = c_to_xy(c)
                cv2.circle(board, (x, y), CHOICE_RADIUS, CHOICE_COLOR, CHOICE_THICKNESS)
                cv2.putText(board, str(i+1), (x + CHOICE_RADIUS, y - CHOICE_RADIUS), CHOICE_FONT, CHOICE_FONTSCALE, CHOICE_COLOR, CHOICE_THICKNESS, cv2.LINE_AA)

        h, w = board.shape[:2]
        nw = 1000
        w, h = nw, int(h * nw/w)
        board = cv2.resize(board, (w, h))

        # cv2.imshow("M", board)
        # cv2.waitKey(3000)
        # cv2.destroyAllWindows()

        cv2.imwrite(self.current_map_img, board)
        
    def get_possible_choices(self, og, building):
        def road():
            start = og.get_starting_house()
            if not start:
                return []

            possible = []

            for e in find_neighbours(start.c):
                if not self.get_building(e):
                    possible.append(e)
            
            for r in og.get_roads():
                for v in find_neighbours(r.c):
                    for e in find_neighbours(v):
                        exists = False
                        for x in find_equivalent(e, include_c=True):
                            if x in possible:
                                exists = True
                                break

                        if not self.get_building(e) and not exists:
                            possible.append(e)

            return possible

        def house():
            possible = []

            for r in og.get_roads():
                for v in find_neighbours(r.c):
                    if can_build_house(self, v):
                        exists = False

                        for p in possible:
                            if check_equivalent(v, p):
                                exists = True
                                break
                                
                        if not exists:
                            possible.append(v)

            return possible
        
        def village():
            return [b.c for b in og.get_houses()]

        cases = {
            B_ROAD: road,
            B_HOUSE: house,
            B_VILLAGE: village
        }

        choices = cases[building.name]()
        return choices

    def add_transparent_image(self, background, foreground, x_offset=None, y_offset=None):
        bg_h, bg_w, bg_channels = background.shape
        fg_h, fg_w, fg_channels = foreground.shape

        assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found: {bg_channels}'
        assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found: {fg_channels}'

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
