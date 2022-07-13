"""
user functions:
- view full overview
> full resources count
> score count
- buy a building
- buy a powerup card
- view powerup cards
- use powerup cards
"""

from telegram import BotCommand
from bot_needs.comm import get_chat_id, BOT_COMM
from constants.bot.common import COMM_COUT, COMM_CIN
from objects.Building import Building
import globals.env as g_env


def get_user_og(ogs, chat_id):
    for og in ogs.keys():
        if ogs[og].active_id == chat_id:
            return og


async def overview(update, context):
    chat_id = get_chat_id(update)
    og = get_user_og(g_env.OGS, chat_id)
    resources = g_env.OGS[og].get_resources()
    scores = g_env.OGS[og].calculate_points()
    text = "Your OG's resources:\n"
    for resource, value in resources.items():
        text += f'{resource}: {value} '
    text += f'\nYour points: {scores}'

    await BOT_COMM(chat_id, COMM_COUT, text)


async def buy_building(update, context):
    chat_id = get_chat_id(update)
    og = get_user_og(g_env.OGS, chat_id)

    async def on_resp_resource_set(type, set):
        pass

    async def on_resp_building_type(type):
        b = Building()
        b.set_name(type)
        b.owner = og.name
        r_sets = b.try_build(og)
        choices = g_env.MAP.get_possible_choices(og, b)
        if not choices:
            await BOT_COMM(chat_id, COMM_COUT, "No options available.")
        elif not r_sets:
            await BOT_COMM(chat_id, COMM_COUT, "Cannot afford building.")
        else:
            await BOT_COMM(chat_id, COMM_CIN, )

    await BOT_COMM(chat_id, COMM_CIN, "", options=on_resp_building_type)


async def buy_powerup_card(update, context):
    pass


async def view_powerup_cards(update, context):
    pass


async def use_powerup_card(update, context):
    pass

BOTCOMMANDS_OG = [
    BotCommand(
        'overview', 'Get an overview of your current OG\'s resources and points.'),
    BotCommand('buybuilding', 'Buy a building and place it on the map.'),
    BotCommand('buypowerupcard', 'Buy a powerup card.'),
    BotCommand('viewpowerupcards', 'View all unused powerup cards.'),
    BotCommand('usepowerupcard', 'Use an unused powerup card.'),
]
COMMAND_HANDLERS_OG = {
    'overview': overview,
    'buybuilding': buy_building,
    'buypowerupcard': buy_powerup_card,
    'viewpowerupcards': view_powerup_cards,
    'usepowerupcard': use_powerup_card
}
