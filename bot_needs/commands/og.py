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
from constants.names import B_HOUSE, B_LIST, B_ROAD, B_VILLAGE
from objects.Building import Building
import globals.env as g_env
import globals.bot as g_bot


def get_user_og(chat_id):
    for og in g_env.OGS.values():
        if og.active_id == chat_id:
            return og

    return None

async def overview(update, context):
    chat_id = get_chat_id(update)
    og = get_user_og(chat_id)
    resources = og.get_resources()
    scores = og.calculate_points()
    text = "Your OG's resources:\n"
    for resource, value in resources.items():
        text += f'{resource}: {value} '
    text += f'\nYour points: {scores}'

    await BOT_COMM(chat_id, COMM_COUT, text)


async def buy_building(update, context):
    chat_id = get_chat_id(update)
    og = get_user_og(chat_id)
    b = Building()
    choices = None

    async def on_resp_building_loc(type, set, loc):
        if og.buy_building(b, r_set=set):
            g_env.MAP.place_building(choices[int(loc) - 1], b)
            await BOT_COMM(chat_id, COMM_COUT, f"Building of type {type} placed at location {loc}.")
        else:
            await BOT_COMM(chat_id, COMM_COUT, "Purchase failed for unknown reasons.")

    async def on_resp_resource_set(type, set):
        g_env.MAP.generate_map_img(choices)
        await g_bot.STATE.send_image(chat_id, g_env.MAP.current_map_img)
        await BOT_COMM(chat_id, COMM_CIN, f"Where do you want to build a {type}?", options=list(range(1, len(choices) + 1)), on_response=lambda loc: on_resp_building_loc(type, set, loc))

    async def on_resp_building_type(type):
        b.set_name(type)
        b.owner = og.name
        r_sets = b.try_build(og)

        nonlocal choices
        choices = g_env.MAP.get_possible_choices(og, b)

        if not choices:
            await BOT_COMM(chat_id, COMM_COUT, "No locations available.")
        elif not r_sets:
            await BOT_COMM(chat_id, COMM_COUT, "Cannot afford building.")
        else:
            price_list = b.get_price_list()
            r_options = [", ".join([f'{p} {r}' for p, r in zip(price_list, r_set)]) for r_set in r_sets]
            await BOT_COMM(chat_id, COMM_CIN, "Select resource set:", options=r_options, on_response=lambda set: on_resp_resource_set(type, r_sets[r_options.index(set)]))

    await BOT_COMM(chat_id, COMM_CIN, "Please enter building type.", options=B_LIST, on_response=on_resp_building_type)

async def buy_powerup_card(update, context):
    pass


async def view_powerup_cards(update, context):
    pass

async def use_powerup_card(update, context):
    pass

BOTCOMMANDS_OG = [
    BotCommand('overview', 'Get an overview of your current OG\'s resources and points.'),
    BotCommand('buybuilding', 'Buy a building and place it on the map.'),
    BotCommand('buypowerupcard', 'Buy a powerup card.'),
    BotCommand('viewpowerupcards', 'View all unused powerup cards.'),
    BotCommand('usepowerupcard', 'Use an unused powerup card.')
]
COMMAND_HANDLERS_OG = {
    'overview': overview,
    'buybuilding': buy_building,
    'buypowerupcard': buy_powerup_card,
    'viewpowerupcards': view_powerup_cards,
    'usepowerupcard': use_powerup_card
}
