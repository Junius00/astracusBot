from constants.names import B_HOUSE, B_VILLAGE, B_ROAD, KEY_R, OG_AVARI, R_WHEAT, R_WATER, R_WOOD, R_MINERAL
from objects.Building import Building
from objects.Map import Map
from objects.OG import OG

def test_build_combinations():
    og = OG(OG_AVARI, R_WHEAT)
    print(og.items)
    b = Building(B_VILLAGE)
    [print(x) for x in b.try_build(og)]

def test_map():
    map = Map()
    map.generate_map()

test_build_combinations()