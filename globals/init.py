from constants.days import DAY1_START, DAY2_START, DAY3_START
import globals.bot as g_bot
import globals.env as g_env
from objects.BotState import BotState
from objects.OG import OG
from objects.Map import Map
from objects.Building import Building
from constants.names import B_HOUSE
from constants.map.positions import START_AVARI, START_KELGRAS, START_LEVIATHAN, START_THERON
from constants.powerups import PUP_INFO
from scheduling import schedule_dt
from datetime import datetime as dt, timedelta

def schedule_tasks():
    #reset flags lost at the end of every day
    def revert_flags_lost():
        print(f'Running scheduled flag reverting at {dt.now()}')
        for og in g_env.OGS.values():
            og.flags_lost = 0
    
    schedule_dt(DAY1_START, revert_flags_lost)
    schedule_dt(DAY2_START, revert_flags_lost)
    schedule_dt(DAY3_START, revert_flags_lost)

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

    g_env.PUP_TRACKER = PUP_INFO()
    
    g_bot.STATE = BotState(app)
    schedule_tasks()