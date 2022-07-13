import globals.bot as g_bot
import globals.env as g_env
from objects.BotState import BotState
from objects.OG import OG
from objects.Map import Map
from objects.Building import Building
from constants.names import B_HOUSE
from constants.map.positions import START_AVARI, START_KELGRAS, START_LEVIATHAN, START_THERON


def init_global(app):
    for og in g_env.OGS.keys():
        g_env.OGS[og] = OG(og)

    g_env.MAP = Map()
    starts = [START_AVARI, START_KELGRAS, START_LEVIATHAN, START_THERON]

    for og, c in zip(g_env.OGS.values(), starts):
        b = Building()
        b.set_name(B_HOUSE)

        og.set_starting_house(b)
        g_env.MAP.place_building(c, b)

    g_bot.STATE = BotState(app)
