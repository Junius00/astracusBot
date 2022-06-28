from constants.buildings import B_POINTS, B_RATIOS

class Building():
    def __init__(self, name):
        self.name = name
        self.points = B_POINTS[name]
        self.ratio = B_RATIOS[name]

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
            if len(p_others) == 0 or len(r_others) == 0:
                paths.append(path)
                return None
            
            p_cur, p_rem = p_others[0], p_others[1:]

            for i, r in enumerate(r_others):
                if res[r] < p_cur:
                    continue
                
                new_path = path.copy()
                new_path.append(r)

                r_copy = r_others.copy()
                del r_copy[i]
                get_path(new_path, p_rem, r_copy)

        get_path([og.dominant_r], p_others, r_others)        
        return paths if len(paths) > 0 else None



