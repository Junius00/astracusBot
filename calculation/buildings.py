from calculation.grid import check_equivalent, find_neighbours


def can_build_house(map, c):
    if map.get_building(c):
        return False

    edges = find_neighbours(c)

    for e in edges:
        out_v = find_neighbours(e)

        for v in out_v:
            if check_equivalent(c, v):
                continue
                
            if map.get_building(v):
                return False
    
    return True