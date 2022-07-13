from ast import literal_eval
import json
from calculation.arrays import nCr
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
        return [self.ratio[0], *self.ratio[1]]
    
    #returns a list of possible resource combinations to build if possible, else returns None
    def try_build(self, og):
        res = og.get_resources()
        r_others = og.get_other_r_keys()

        p_own, p_others = self.ratio
        if res[og.dominant_r] < p_own:
            #cannot afford own, return None
            return None
        
        paths = []
        def get_path(path, p_others, r_others):
            if len(p_others) == 0:
                paths.append(path)
                return None
            
            p_cur, p_rem = p_others[0], p_others[1:]
            cur_count = 1
            while p_rem and p_cur == p_rem[0]:
                p_rem = p_rem[1:]
                cur_count += 1
            
            for i, r_set in enumerate(nCr(r_others, cur_count)):
                should_add = True
                for r in r_set:
                    if res[r] < p_cur:
                        should_add = False
                        break

                if not should_add:
                    continue

                new_path = path.copy() + r_set
                r_copy = [x for x in r_others if x not in r_set]

                get_path(new_path, p_rem, r_copy)

        get_path([og.dominant_r], p_others, r_others)        
        return paths if paths else None
    
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