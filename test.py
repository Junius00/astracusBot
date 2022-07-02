from random import choice, randint
from calculation.grid import check_equivalent, find_equivalent, find_neighbours, is_valid
from constants.map.axes import MAP_E_OFFSET, MAP_QLIM, MAP_RLIM, MAP_SLIM
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

        if i > 9:
            choices.append(c)
            continue

        bname = choice([B_ROAD, B_HOUSE, B_VILLAGE])
        bowner = choice([OG_AVARI, OG_KELGRAS, OG_LEVIATHAN, OG_THERON])

        if bname == B_ROAD:
            a += MAP_E_OFFSET
        b = Building()
        b.owner = bowner

        b.set_name(bname)

        map.place_building((q, r, s, a), b)

    for k, v in map.map.items():
        print(f'{k}: {v.owner} {v.name}')

    map.generate_map_img(choices=choices)
    

def test_c():
    while True:
        i = input('Enter q,r,s,a: ')
        c = tuple([int(x) for x in i.split(',')])
        print(find_neighbours(c))

#test_build_combinations()
test_map()
#test_c()