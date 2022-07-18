from constants.days import DAY1_END, DAY1_START, DAY2_END, DAY2_START, DAY3_END, DAY3_START
import globals.bot as g_bot
import globals.env as g_env
from objects.BotState import BotState
from objects.OG import OG
from objects.Map import Map
from constants.powerups import PUP_INFO

from scheduling import schedule_dt, schedule_dt_async
from scheduling.tasks import add_command_desc, clear_pending_actions, make_backup, revert_flags_lost, switch_fools_luck

from powerups.allocation import load_pups


def schedule_tasks():
    # reset flags lost at the end of every day
    schedule_dt(DAY1_END, revert_flags_lost)
    schedule_dt(DAY2_END, revert_flags_lost)
    schedule_dt(DAY3_END, revert_flags_lost)

    # switch Fool's Luck to Day 3 action
    schedule_dt_async(DAY3_START, switch_fools_luck)

    # add new commands on Day 3
    schedule_dt_async(DAY3_START, add_command_desc)

    # clear all pending actions
    clear_pending_actions()

    # initialise backup sequence
    make_backup()


def init_global(app):
    for og in g_env.OGS.keys():
        g_env.OGS[og] = OG(og)

    g_env.MAP = Map()

    g_env.PUP_TRACKER = load_pups()

    g_bot.STATE = BotState(app)
