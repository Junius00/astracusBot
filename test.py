from random import choice, randint
from calculation.grid import check_equivalent, find_equivalent, find_neighbours, is_valid
from constants.map.axes import MAP_E_OFFSET, MAP_QLIM, MAP_RLIM, MAP_SLIM
from constants.map.positions import START_AVARI, START_KELGRAS, START_LEVIATHAN, START_THERON
from constants.names import B_HOUSE, B_VILLAGE, B_ROAD, KEY_R, OG_AVARI, OG_KELGRAS, OG_LEVIATHAN, OG_THERON, R_WHEAT, R_WATER, R_WOOD, R_MINERAL
from objects.Building import Building
from objects.Map import Map
from objects.OG import OG

def test_build_combinations():
    og = OG(OG_AVARI, R_WHEAT)
    print(og.items)
    b = Building()
    [print(x) for x in b.try_build(og)]

def test_map():
    def c_gen():
        q = randint(-MAP_QLIM, MAP_QLIM)
        r = randint(-MAP_RLIM, MAP_RLIM)
        s = -q-r
        a = 60 * randint(0, 5)
        return q, r, s, a

    map = Map()
    choices = []
    for i in range(12):
        c = c_gen()
        while not is_valid(c):
            c = c_gen()

        q, r, s, a = c

        #bname = choice([B_ROAD, B_HOUSE, B_VILLAGE])
        bname = B_ROAD
        bowner = choice([OG_AVARI, OG_KELGRAS, OG_LEVIATHAN, OG_THERON])

        if bname == B_ROAD:
            a += MAP_E_OFFSET

        c = q, r, s, a
        if i > 9:
            print(i-9, c, bname)
            choices.append(c)
            continue
    
        b = Building()
        b.owner = bowner

        b.set_name(bname)

        map.place_building(c, b)

    for k, v in map.map.items():
        print(f'{k}: {v.owner} {v.name}')

    map.generate_map_img(choices=choices)
    
def test_build_map():
    map = Map()

    ogs = [OG(OG_AVARI), OG(OG_KELGRAS), OG(OG_LEVIATHAN), OG(OG_THERON)]
    starts = [START_AVARI, START_KELGRAS, START_LEVIATHAN, START_THERON]
    buildings = [Building(), Building(), Building(), Building()]

    for og, c, b in zip(ogs, starts, buildings):
        print(b.to_obj())
        b.set_name(B_HOUSE)

        og.set_starting_house(b)
        map.place_building(c, b)
    
    for b in buildings:
        print(b.to_obj())

    for og in ogs:
        print(og.name, og.get_houses()[0].to_obj())

    while True:
        for og in ogs:
            print(og.name)
            print("""
            1. ROAD
            2. HOUSE
            3. VILLAGE
            """)
            choice = [B_ROAD, B_HOUSE, B_VILLAGE][int(input('>> ')) - 1]
            
            b = Building()
            b.set_name(choice)

            map.get_possible_map(og, b)

def test_c():
    while True:
        i = input('Enter q,r,s,a: ')
        c = tuple([int(x) for x in i.split(',')])
        print(find_neighbours(c))

#test_build_combinations()
test_build_map()
#test_c()