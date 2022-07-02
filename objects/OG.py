import json
import os
from constants.names import B_HOUSE, B_ROAD, B_VILLAGE, KEY_B, KEY_P, KEY_R, R_MINERAL, R_WATER, R_WHEAT, R_WOOD
from constants.storage import FOLDER_DATA
from constants.templates import B_TEMPLATE, P_TEMPLATE, R_TEMPLATE


class OG():
    def __init__(self, name, dominant_r_key):
        self.name = name
        self.filename = os.path.join(FOLDER_DATA, f'{name}.json')
        self.dominant_r = dominant_r_key
        self.items = self.load_from_json()

    def load_from_json(self):
        if os.path.exists(self.filename):
            f = open(self.filename, 'r')
            res = json.load(f)
            f.close()

            return res
        
        return {
            KEY_B: B_TEMPLATE,
            KEY_R: R_TEMPLATE,
            KEY_P: P_TEMPLATE
        }
    
    def save_to_json(self):
        with open(self.filename, 'w') as f:
            json.dump(self.items, f)

    def get_other_r_keys(self):
        return [x for x in [R_WHEAT, R_MINERAL, R_WATER, R_WOOD] if x != self.dominant_r]
    
    def get_resources(self):
        return self.items[KEY_R]

    def add_resource(self, r_key, amount):
        self.items[KEY_R][r_key] += amount
    
    #returns True and uses if possible, otherwise False and no change
    def use_resource(self, r_key, amount):
        cur = self.items[KEY_R][r_key]

        if cur < amount:
            return False
        
        self.items[KEY_R][r_key] -= amount
        return True

    #returns True if possible, otherwise False and no change
    def buy_building(self, r_set, building):
        old_res = self.items[KEY_R].copy()

        prices = [building.ratio[0], *building.ratio[1]]
        for i, r in enumerate(r_set):
            success = self.use_resource(r, prices[i])
            
            #revert immediately if fail
            if not success:
                self.items[KEY_R] = old_res
                return False
        
        self.items[KEY_B][building.name] += 1
        return True

    def calculate_points(self):
        summary = ""
        

    def use_modifier(self, modifier_function, *args, **kwargs):
        modifier_function(self, *args, **kwargs)