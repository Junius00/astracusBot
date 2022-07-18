import os
import json
from datetime import datetime as dt, timedelta
from bot_needs.comm import BOT_COMM
from bot_needs.commands.admin import BOTCOMMANDS_ADMIN, BOTCOMMANDS_ADMIN_DAY3
from bot_needs.commands.common import BOTCOMMANDS_COMMON
from bot_needs.commands.og import BOTCOMMANDS_OG, BOTCOMMANDS_OG_DAY3
from constants.bot.common import COMM_COUT
from constants.names import KEY_PUP_ACTION, KEY_PUP_DESC, KEY_PUP_QUANTITY, PUP_FOOLS_LUCK
from constants.storage import FOLDER_DATA, PUP_FILENAME
import globals.bot as g_bot
import globals.env as g_env
from powerups.actions import fools_luck_day3
from scheduling import schedule_dt

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
            await BOT_COMM(og.active_id, COMM_COUT, alert_msg, is_end_of_sequence=False)

# clear all actions if OG is free
def clear_pending_actions(interval_s=5):
    g_bot.STATE.do_all_actions()

    schedule_dt(dt.now() + timedelta(seconds=interval_s),
                clear_pending_actions, interval_s=interval_s)

# Makes backup for whatever needs it
def make_backup(interval_s=10):
    print(f'Making backup at {dt.now()}')

    for og in g_env.OGS.values():
        og.save_to_json()
    g_env.MAP.save_to_json()
    pups = {}
    for key, dic in g_env.PUP_TRACKER.items():
        pups[key] = dic[KEY_PUP_QUANTITY]
    with open(PUP_FILENAME, 'w') as f:
        json.dump(pups, f)

    schedule_dt(dt.now() + timedelta(seconds=interval_s),
                make_backup, interval_s=interval_s)

# Switches command descriptions on Day 3
async def add_command_desc():
    print(f'Updating commands at {dt.now()}')
    c_admin = BOTCOMMANDS_COMMON + BOTCOMMANDS_ADMIN + BOTCOMMANDS_ADMIN_DAY3
    c_og = BOTCOMMANDS_COMMON + BOTCOMMANDS_OG + BOTCOMMANDS_OG_DAY3

    await g_bot.STATE.update_admin_command_desc(c_admin)
    for og in g_env.OGS.values():
        await og.update_command_desc(c_og)