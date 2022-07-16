import os
import json
from datetime import datetime as dt, timedelta
from bot_needs.comm import BOT_COMM
from constants.bot.common import COMM_COUT
from constants.names import KEY_PUP_ACTION, KEY_PUP_DESC, KEY_PUP_QUANTITY, PUP_FOOLS_LUCK
from constants.storage import FOLDER_DATA
import globals.bot as g_bot
import globals.env as g_env
from powerups.actions import fools_luck_day3
from scheduling import schedule_dt

PUP_FILENAME = os.path.join(FOLDER_DATA, 'pups.json')

# reset flags lost for all OGs


def revert_flags_lost():
    print(f'Running scheduled flag reverting at {dt.now()}')
    for og in g_env.OGS.values():
        og.flags_lost = 0

# change Fool's Luck action and notify all


async def switch_fools_luck():
    print(f'Running scheduled Fool\'s Luck switching at {dt.now()}')
    g_env.PUP_TRACKER[PUP_FOOLS_LUCK][KEY_PUP_ACTION] = fools_luck_day3
    g_env.PUP_TRACKER[PUP_FOOLS_LUCK][KEY_PUP_DESC] = 'Activate this card before the next mass game. If your tribe wins the next mass game, you will gain 50% more structures from the amount of collateral the losing tribe has put down.'

    alert_msg = """A twist to Fool's Luck! Instead of receiving extra resources, your total earnings will be determined by the amount of collateral you put down for each game. If your tribe wins the mass game you have selected to use this card on, you will gain 50% more structures from the amount of collateral the losing tribe has put down. For example:

For an even number of collateral put down, the winning tribe will gain 50% more.

For odd number of collateral put down, the following allocation system will be followed:
    - If losing tribe puts down 1 house as collateral, your tribe will gain 1 extra road
    - If losing tribe puts down 1 village as collateral, your tribe will gain 1 extra house
"""
    for og in g_env.OGS.values():
        if og.has_powerup(PUP_FOOLS_LUCK):
            await BOT_COMM(og.active_id, COMM_COUT, alert_msg)

# clear all actions if OG is free


def clear_pending_actions(interval_s=5):
    g_bot.STATE.do_all_actions()

    schedule_dt(dt.now() + timedelta(seconds=interval_s),
                clear_pending_actions)

# Makes backup for whatever needs it

def make_backup():
    print(f'Making backup.')
    for og in g_env.OGS.values():
        og.save_to_json()
    g_env.MAP.save_to_json()
    pups = {}
    for key, dic in g_env.PUP_TRACKER.items():
        pups[key] = dic[KEY_PUP_QUANTITY]
    with open(PUP_FILENAME, 'w') as f:
        json.dump(pups, f)
    