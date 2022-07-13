#generates all possible nCr combinations from an array
def nCr(arr, r):
    combis = []

    def combi_gen(combi, rem, r):
        if r == 0:
            combis.append(combi)
            return

        if not rem:
            return
        
        left = len(rem) - r
        for i, x in enumerate(rem):
            new_combi = combi.copy() + [x]
            combi_gen(new_combi, rem[i+1:], r-1)

    combi_gen([], arr, r)
    return combis

def get_r_paths(ratio, og):
    res = og.get_resources()
    r_others = og.get_other_r_keys()

    p_own, p_others = ratio
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
    
#converts ratio into price list
def ratio_to_price_list(ratio):
    return [ratio[0], *ratio[1]]