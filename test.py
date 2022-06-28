from constants.names import B_HOUSE, B_VILLAGE, B_ROAD, KEY_R, OG_AVARI, R_WHEAT, R_WATER, R_WOOD, R_MINERAL
from objects.Building import Building
from objects.OG import OG

og = OG(OG_AVARI, R_WHEAT)

b = Building(B_VILLAGE)
[print(x) for x in b.try_build(og)]
