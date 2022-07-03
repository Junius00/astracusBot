import json
import os
from constants.names import B_HOUSE, B_ROAD, B_VILLAGE, KEY_B, KEY_P, KEY_R, R_MINERAL, R_WATER, R_WHEAT, R_WOOD
from constants.og import DOMINANT_RESOURCES
from constants.storage import FOLDER_DATA
from constants.templates import B_TEMPLATE, P_TEMPLATE, R_TEMPLATE
from objects.Building import Building


class OG():
    def __init__(self, name):
        self.name = name
        self.filename = os.path.join(FOLDER_DATA, f'{name}.json')
        self.dominant_r = DOMINANT_RESOURCES[name]

        self.load_from_json()

    def reset_items(self):
        self.items = {
            KEY_B: B_TEMPLATE,
            KEY_R: R_TEMPLATE,
            KEY_P: P_TEMPLATE
        }
    
    def set_starting_house(self, house):
        house.owner = self.name
        self.items[KEY_B][B_HOUSE] = [house] + self.items[KEY_B][B_HOUSE]

    def get_starting_house(self):
        houses = self.get_houses()

        if not houses:
            return None
        
        return houses[0]
    
    def get_houses(self):
        return self.items[KEY_B][B_HOUSE]
    
    def get_roads(self):
        return self.items[KEY_B][B_ROAD]
    
    def get_villages(self):
        return self.items[KEY_B][B_VILLAGE]
    
    def load_from_json(self):
        if os.path.exists(self.filename):
            f = open(self.filename, 'r')
            res = json.load(f)
            f.close()

            res[KEY_B] = {k: [Building().from_obj(b) for b in v] for k, v in res[KEY_B].items()}
            self.items = res
            return
        
        self.reset_items()
    
    def save_to_json(self):
        obj = self.items.copy()
        obj[KEY_B] = {k: [b.to_obj() for b in v] for k, v in obj[KEY_B].items()}

        with open(self.filename, 'w') as f:
            json.dump(obj, f)

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
        for p, r in zip(prices, r_set):
            success = self.use_resource(r, p)
            
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