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
from constants.names import B_HOUSE, B_LIST, B_ROAD, B_VILLAGE, KEY_PUP_QUANTITY
from constants.powerups import PUP_JUST_SAY_NO
from objects.Building import Building
import globals.env as g_env
import globals.bot as g_bot
from powerups.allocation import get_random_pup


def get_user_og(chat_id):
    for og in g_env.OGS.values():
        if og.active_id == chat_id:
            return og

    return None

async def alert_unregistered(chat_id):
    await BOT_COMM(chat_id, COMM_COUT, 'It seems you are not registered as the active chat for your OG. Please use the active chat for your OG, or use /start to take control.')

async def overview(update, context):
    chat_id = get_chat_id(update)
    og = get_user_og(chat_id)

    if not og:
        await alert_unregistered(chat_id)
        return
    
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

    if not og:
        await alert_unregistered(chat_id)
        return
    
    b = Building()
    choices = None

    async def on_resp_building_loc(type, set, loc):
        if og.buy_building(b, r_set=set):
            g_env.MAP.place_building(choices[int(loc) - 1], b)
            await BOT_COMM(chat_id, COMM_COUT, f"Building of type {type} placed at location {loc}.")
        else:
            await BOT_COMM(chat_id, COMM_COUT, "Purchase failed for unknown reasons.")

    async def on_resp_resource_set(type, set):
        map_img = g_env.MAP.generate_map_img(choices)
        await g_bot.STATE.send_image(chat_id, map_img)
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
    chat_id = get_chat_id(update)
    og = get_user_og(chat_id)

    if not og:
        await alert_unregistered(chat_id)
        return
        
    pup = get_random_pup()
    if not pup:
        await BOT_COMM(chat_id, COMM_COUT, 'There are no powerup cards left to buy.')
        return

    r_sets = pup.try_build(og)
    if not r_sets:
        await BOT_COMM(chat_id, COMM_COUT, 'You don\'t have enough resources to build a powerup card. Please try again later.')
        return
    
    async def on_resp_r_set(r_set):
        nonlocal pup

        if og.buy_powerup(pup, r_set):
            if g_env.PUP_TRACKER[pup.name][KEY_PUP_QUANTITY] < 1:
                pup = get_random_pup()
                if not pup:
                    await BOT_COMM(chat_id, COMM_COUT, 'Oops! It appears someone has snatched the last card before you could. Better luck next time!')
                    return
            
            g_env.PUP_TRACKER[pup.name][KEY_PUP_QUANTITY] -= 1
            await BOT_COMM(chat_id, COMM_COUT, f'You have successfully obtained {pup.name}.\n{pup.desc}')

            if pup.is_instant:
                await BOT_COMM(chat_id, COMM_COUT, f'{pup.name} is instantly activated.')
                await pup.activate(g_env.MAP, og, [og_name for og_name in g_env.OGS.keys() if og_name != og.name])
            
            return
        
        await BOT_COMM(chat_id, COMM_COUT, 'Purchase has failed. Please try again later.')
    
    r_options = [", ".join([f'{p} {r}' for p, r in zip(pup.get_price_list(), r_set)]) for r_set in r_sets]
    await BOT_COMM(chat_id, COMM_CIN, 'Select resource set:', options=r_options, on_response=lambda set: on_resp_r_set(r_sets[r_options.index(set)]))

async def view_powerup_cards(update, context):
    chat_id = get_chat_id(update)
    og = get_user_og(chat_id)

    if not og:
        await alert_unregistered(chat_id)
        return

    pups = og.get_powerups()
    if not pups and not og.can_say_no():
        await BOT_COMM(chat_id, COMM_COUT, 'You have no powerup cards available for use.')
        return

    pups_str = 'Powerup Cards Available:\n' + '\n'.join([f'{pup.name}: {pup.desc}' for pup in pups])
    
    if og.can_say_no():
        pups_str += f'\nNumber of {PUP_JUST_SAY_NO} cards: {og.just_say_no_count}\n'

    await BOT_COMM(chat_id, COMM_COUT, pups_str)

async def use_powerup_card(update, context):
    chat_id = get_chat_id(update)
    og = get_user_og(chat_id)

    if not og:
        await alert_unregistered(chat_id)
        return

    pups = og.get_powerups()
    if not pups:
        await BOT_COMM(chat_id, COMM_COUT, 'You have no powerup cards available for use.')
        return
    
    pups_str = 'Powerup Cards Available:\n' + '\n'.join([f'({i+1}) {pup.name}: {pup.desc}' for i, pup in enumerate(pups)])

    async def on_resp_use(option):
        option = int(option) - 1
        await og.use_powerup(option)
        #await BOT_COMM(chat_id, COMM_COUT, 'Powerup card successfully used.')

    await BOT_COMM(chat_id, COMM_CIN, pups_str, options=list(range(1, len(pups) + 1)), on_response=on_resp_use)

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
