"""
user functions:
- view full overview
> full resources count
> score count
- buy a building
- buy a powerup card
- view powerup cards
- use powerup cards
- view collateral buildings
- place collateral buildings (requires roads to place)
"""

from telegram import BotCommand
from bot_needs.comm import BOT_MAP, get_chat_id, BOT_COMM
from bot_needs.commands.alerts import alert_unregistered, alerted_map_lock
from constants.bot.common import COMM_COUT, COMM_CIN
from constants.names import B_HOUSE, B_LIST, B_VILLAGE, KEY_PUP_QUANTITY
from constants.powerups import PUP_JUST_SAY_NO
from objects.Building import Building
import globals.env as g_env
from powerups.allocation import get_random_pup


def get_user_og(chat_id):
    for og in g_env.OGS.values():
        if og.active_id == chat_id:
            return og

    return None

async def overview(update, context):
    chat_id = get_chat_id(update)
    og = get_user_og(chat_id)

    if not og:
        await alert_unregistered(chat_id)
        return
    
    text = "Your OG's resources:\n"
    text += og.pretty_print_resources()
    scores = og.calculate_points()
    text += f'\nYour points: {scores}'

    await BOT_COMM(chat_id, COMM_COUT, text)


async def buy_building(update, context):
    chat_id = get_chat_id(update)
    og = get_user_og(chat_id)

    if not og:
        await alert_unregistered(chat_id)
        return
    
    if await alerted_map_lock(chat_id):
        return
    
    b = Building()
    choices = None

    async def on_resp_building_loc(type, set, loc):
        if og.buy_building(b, r_set=set):
            c = choices[int(loc) - 1]
            existing_b = g_env.MAP.get_building(c)
            if existing_b:
                g_env.MAP.remove_building(existing_b)
                og.delete_building(existing_b)

            g_env.MAP.place_building(c, b)
            await BOT_COMM(chat_id, COMM_COUT, f"Building of type {type} placed.")
            await BOT_MAP(chat_id)
        else:
            await BOT_COMM(chat_id, COMM_COUT, "Purchase failed. Please try again later.")

        g_env.MAP.unlock()

    async def on_resp_resource_set(type, set):
        await BOT_MAP(chat_id, choices)
        await BOT_COMM(chat_id, COMM_CIN, f"Where do you want to build a {type}?", options=list(range(1, len(choices) + 1)), on_response=lambda loc: on_resp_building_loc(type, set, loc))

    async def on_resp_building_type(type):
        b.set_name(type)
        b.owner = og.name
        r_sets = b.try_build(og)

        nonlocal choices
        choices = g_env.MAP.get_possible_choices(og, b)

        if not choices:
            await BOT_COMM(chat_id, COMM_COUT, "No locations available.")
            g_env.MAP.unlock()
        elif not r_sets:
            await BOT_COMM(chat_id, COMM_COUT, "Cannot afford building.")
            g_env.MAP.unlock()
        else:
            price_list = b.get_price_list()
            r_options = [", ".join([f'{p} {r}' for p, r in zip(price_list, r_set)]) for r_set in r_sets]
            await BOT_COMM(chat_id, COMM_CIN, f"Select resource set:\n\nCurrent Resources:\n{og.pretty_print_resources()}", options=r_options, on_response=lambda set: on_resp_resource_set(type, r_sets[r_options.index(set)]))

    g_env.MAP.lock()
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
                await pup.activate(og)
                og.used_powerups += 1
            
            return
        
        await BOT_COMM(chat_id, COMM_COUT, 'Purchase has failed. Please try again later.')
    
    r_options = [", ".join([f'{p} {r}' for p, r in zip(pup.get_price_list(), r_set)]) for r_set in r_sets]
    await BOT_COMM(chat_id, COMM_CIN, f"Select resource set:\n\nCurrent Resources:\n{og.pretty_print_resources()}", options=r_options, on_response=lambda set: on_resp_r_set(r_sets[r_options.index(set)]))

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

async def view_collateral_buildings(update, context):
    chat_id = get_chat_id(update)
    og = get_user_og(chat_id)

    if not og:
        await alert_unregistered(chat_id)
        return
    
    if not og.collateral_buildings:
        await BOT_COMM(chat_id, COMM_COUT, 'You have no collateral buildings to place at the moment.')
        return
    
    await BOT_COMM(chat_id, COMM_COUT, f'Remaining unplaced collateral:\n{og.pretty_print_collateral_buildings()}')

async def place_collateral_buildings(update, context):
    chat_id = get_chat_id(update)
    og = get_user_og(chat_id)

    if not og:
        await alert_unregistered(chat_id)
        return
    
    if not og.collateral_buildings:
        await BOT_COMM(chat_id, COMM_COUT, 'You have no collateral buildings to place at the moment.')
        return
    
    if await alerted_map_lock(chat_id):
        return
    
    skip = 0

    async def on_resp_loc(building, c):
        existing_b = g_env.MAP.get_building(c)
        if existing_b:
            g_env.MAP.remove_building(existing_b)
            og.delete_building(existing_b)

        g_env.MAP.place_building(c, building)
        del og.collateral_buildings[skip]

        await BOT_COMM(chat_id, COMM_COUT, f"Building of type {type} placed.")
        await BOT_MAP(chat_id)

        bslice = og.collateral_buildings[skip:]
        if bslice:
            await place_building(bslice[0])
            return
        
        g_env.MAP.unlock()
        await BOT_COMM(chat_id, COMM_COUT, f'Placed all possible collateral buildings.\n\nRemaining unplaced collateral:\n{og.pretty_print_collateral_buildings()}')

    async def place_building(b):
        choices = []
        if b.name == B_VILLAGE:
            choices += g_env.MAP.get_possible_choices(og, b, override_building_type=B_HOUSE)
        
        choices += g_env.MAP.get_possible_choices(og, b)

        if not choices:
            nonlocal skip
            skip += 1
            return
        
        await BOT_MAP(chat_id, choices)
        await BOT_COMM(chat_id, COMM_CIN, f'Please choose a location to place your new {b.name}.', options=list(range(1, len(choices) + 1)), on_response=lambda choice: on_resp_loc(b, choices[int(choice) - 1]))

    g_env.MAP.lock()
    await place_building(og.collateral_buildings[0])

BOTCOMMANDS_OG = [
    BotCommand('overview', 'Get an overview of your current OG\'s resources and points.'),
    BotCommand('buybuilding', 'Buy a building and place it on the map.'),
    BotCommand('buypowerupcard', 'Buy a powerup card.'),
    BotCommand('viewpowerupcards', 'View all unused powerup cards.'),
    BotCommand('usepowerupcard', 'Use an unused powerup card.'),
    BotCommand('viewcollateralbuildings', 'View all unplaced collateral buildings.'),
    BotCommand('placecollateralbuildings', 'Put down buildings won as collateral from games (if possible).')
]
COMMAND_HANDLERS_OG = {
    'overview': overview,
    'buybuilding': buy_building,
    'buypowerupcard': buy_powerup_card,
    'viewpowerupcards': view_powerup_cards,
    'usepowerupcard': use_powerup_card,
    'viewcollateralbuildings': view_collateral_buildings,
    'placecollateralbuildings': place_collateral_buildings
}
