from ast import literal_eval
import json
from calculation.arrays import get_r_paths, nCr, ratio_to_price_list
from calculation.grid import check_equivalent
from constants.buildings import B_POINTS, B_RATIOS, KEY_C, KEY_CONNECTED, KEY_NAME, KEY_OWNER

class Building():
    def __init__(self):
        self.name = None
        self.owner = None
        self.c = None

    def set_name(self, name):
        self.name = name
        self.points = B_POINTS[name]
        self.ratio = B_RATIOS[name]
    
    def get_price_list(self):
        return ratio_to_price_list(self.ratio)
    
    #returns a list of possible resource combinations to build if possible, else returns None
    def try_build(self, og):
        return get_r_paths(self.ratio, og)
    
    def to_obj(self):
        return {
            KEY_NAME: self.name,
            KEY_OWNER: self.owner,
            KEY_C: str(self.c)
        }
    
    def from_obj(self, obj):
        self.set_name(obj[KEY_NAME])
        self.owner = obj[KEY_OWNER]
        self.c = literal_eval(obj[KEY_C])

        return self

    def clone(self, building):
        self.from_obj(building.to_obj())
        return self
    
    #returns True if it is the same building, else returns False
    def compare(self, building):
        return self.name == building.name and\
            self.owner == building.owner and\
            check_equivalent(self.c, building.c)
            
