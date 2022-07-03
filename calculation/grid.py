# COORDINATES ARE IN (q, r, s, a)
# https://www.redblobgames.com/grids/hexagons/ (cube coordinates)
# a: rotation around hexagon

from constants.map.axes import MAP_E_OFFSET, MAP_EQ_OFFSETS, MAP_QLIM, MAP_RLIM, MAP_ROT, MAP_SLIM, MAP_V_OFFSET

def is_valid(c):
    q, r, s, _ = c

    return abs(q) <= MAP_QLIM \
        and abs(r) <= MAP_RLIM \
        and abs(s) <= MAP_SLIM \
        and q + r + s == 0 \
        and (is_vertex(c) or is_edge(c))

def is_vertex(c):
    return c[3] % 60 == MAP_V_OFFSET

def is_edge(c):
    return c[3] % 60 == MAP_E_OFFSET

def get_offsets(c):
    return MAP_EQ_OFFSETS[int(c[3] / 30)]

def mod_c(c, mod):
    cm = [x + y for x, y in zip(c, mod)]
    cm[3] = cm[3] % 360

    return tuple(cm)

def check_equivalent(c1, c2):
    q1, r1, s1, a1 = c1
    q2, r2, s2, a2 = c2

    if c1 == c2:
        return True
        
    rem1, rem2 = a1 % 60, a2 % 60
    #check for edge/vertex similarity
    if rem1 != rem2:
        return False

    if rem1 == MAP_E_OFFSET: #is edge
        if abs(a1 - a2) != 180:
            return False
        
        calc = [
            q1 == q2,
            r1 == r2,
            s1 == s2
        ]

        return calc[(min(a1, a2) - MAP_E_OFFSET)/MAP_ROT]
    
    #is vertex
    if abs(a1 - a2) % 120 != 0:
        return False
    
    c_sorted = sorted([c1, c2], key= lambda c: c[3])
    (qm, rm, sm, am), (qM, rM, sM, aM) = c_sorted

    calc = {
        (60, 180): qM - qm == 1 and rm - rM == 1 and sm == sM,
        (180, 300): qm == qM and rM - rm == 1 and sm - sM == 1,
        (60, 300): qM - qm == 1 and rm == rM and sm - sM == 1
    }

    return calc[(am, aM)]

def find_equivalent(c):
    if not is_valid(c):
        return []
    
    possible = []
    for offset in get_offsets(c):
        c_new = mod_c(c, offset)

        if is_valid(c_new):
            possible.append(c_new)
    
    return possible

def find_neighbours(c):
    if not is_valid(c):
        return []

    neighbours = [
        mod_c(c, (0, 0, 0, -30)), 
        mod_c(c, (0, 0, 0, 30))
    ]
    if is_edge(c):
        return neighbours
    
    mods = get_offsets(c)
    mods = [mod_c(mods[0], (0, 0, 0, -30)), mod_c(mods[1], (0, 0, 0, 30))]

    for mod in mods:
        c_new = mod_c(c, mod)
        if is_valid(c_new):
            neighbours.append(c_new)
            break
    
    return neighbours

