from ast import literal_eval
import json
from calculation.arrays import get_r_paths, nCr, ratio_to_price_list
from constants.buildings import B_POINTS, B_RATIOS, KEY_C, KEY_CONNECTED, KEY_NAME, KEY_OWNER

class Building():
    def __init__(self):
        self.name = None
        self.owner = None
        self.c = None
        self.connected = []

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
            KEY_C: str(self.c),
            KEY_CONNECTED: [b.to_obj() for b in self.connected]
        }
    
    def from_obj(self, obj):
        self.set_name(obj[KEY_NAME])
        self.owner = obj[KEY_OWNER]
        self.c = literal_eval(obj[KEY_C])
        self.connected = [Building().from_obj(o) for o in obj[KEY_CONNECTED]]