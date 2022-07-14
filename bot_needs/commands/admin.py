"""
admin functions:
- add resource of type
- delete resource of type
- move collateral buildings
- get scores
> individual
> everyone
- view resources
> individual
> everyone
- add misc points (e.g. flag stealing)
"""

import math
from telegram import BotCommand
from bot_needs.comm import BOT_COMM, get_chat_id
from constants.bot.common import COMM_CIN, COMM_COUT
from constants.names import B_LIST, B_ROAD, OGS_LIST, R_LIST
import globals.env as g_env
from objects.Building import Building

async def add_resource(update, context):
    id = get_chat_id(update)

    async def on_resp_number(name, r, count):
        try:
            count = int(count)
        except:
            await BOT_COMM(id, COMM_CIN, 'An invalid amount was entered. Please enter an integer amount (greater than 0) to add.', on_response=lambda count: on_resp_number(name, r, count))
            return
        
        og = g_env.OGS[name]
        added, multi = og.add_resource(r, count)

        await BOT_COMM(id, COMM_COUT, f'{added} {r} has been added to {name} ({multi:.2f}x multiplier applied). [New total: {og.get_resource_count(r)} {r}]')
        await BOT_COMM(og.active_id, COMM_COUT, f'You have earned {added} {r}! ({multi:.2f}x multiplier applied) [New total: {og.get_resource_count(r)} {r}]')

    async def on_resp_resource(name, r):
        await BOT_COMM(id, COMM_CIN, 'Please enter an integer amount (greater than 0) to add.', on_response=lambda count: on_resp_number(name, r, count))

    async def on_resp_og(name):
        if g_env.OGS[name].force_resource:
            r = g_env.OGS[name].force_resource
            await BOT_COMM(id, COMM_COUT, f'{r} has been set as the resource to gain, from previous actions.')
            await on_resp_resource(name, r)
            return
    
        await BOT_COMM(id, COMM_CIN, 'Please choose a resource to add.', options=R_LIST, on_response=lambda r: on_resp_resource(name, r))

    await BOT_COMM(id, COMM_CIN, 'Please choose an OG to add resources for.', options=OGS_LIST, on_response=on_resp_og)
    
async def delete_resource(update, context):
    id = get_chat_id(update)

    async def on_resp_number(name, r, count):
        try:
            count = int(count)
        except:
            await BOT_COMM(id, COMM_CIN, 'An invalid amount was entered. Please enter an integer amount (greater than 0) to remove.', on_response=lambda count: on_resp_number(name, r, count))
            return

        og = g_env.OGS[name]
        og.delete_resource(r, count)
        await BOT_COMM(id, COMM_COUT, f'{count} {r} has been removed from {name}. [New total: {og.get_resource_count(r)} {r}]')
        await BOT_COMM(og.active_id, COMM_COUT, f'{count} {r} has been removed from you! [New total: {og.get_resource_count(r)} {r}]')

    async def on_resp_resource(name, r):
        await BOT_COMM(id, COMM_CIN, 'Please enter an integer amount (greater than 0) to remove.', on_response=lambda count: on_resp_number(name, r, count))

    async def on_resp_og(name):
        await BOT_COMM(id, COMM_CIN, 'Please choose a resource to remove.', options=R_LIST, on_response=lambda r: on_resp_resource(name, r))

    await BOT_COMM(id, COMM_CIN, 'Please choose an OG to add resources for.', options=OGS_LIST, on_response=on_resp_og)

async def move_collateral_buildings(update, context):
    id = get_chat_id(update)

    async def on_resp_move_count(btype, og_name_from, og_name_to, move_count):
        move_count = int(move_count)
        cur = move_count
        avail = g_env.OGS[og_name_from].get_btype(btype)

        while cur > 0:
            b = Building().clone(avail[-1])

            #deregister from map; coordinates removed
            g_env.MAP.remove_building(b)
            #deregister from OG
            if g_env.OGS[og_name_from].delete_building(b):
                #add to winner OG collateral
                g_env.OGS[og_name_to].add_collateral_building(b)

            cur -= 1


        await BOT_COMM(id, COMM_COUT, f'{move_count} {btype}(s) moved from {og_name_from} to {og_name_to}.')            

    async def on_resp_og_to(btype, og_name_from, og_name_to):
        avail = g_env.OGS[og_name_from].get_btype(btype)
        if not avail:
            await BOT_COMM(id, COMM_COUT, f'{og_name_from} does not have {btype}s to give up.')
            return
        
        await BOT_COMM(id, COMM_CIN, f'Please select the number of {btype}s to move.', 
        options=list(range(1, len(avail) + 1)), on_response=lambda move_count: on_resp_move_count(btype, og_name_from, og_name_to, move_count))
        
    async def on_resp_og_from(btype, og_name_from):
        await BOT_COMM(id, COMM_CIN, f'Please select the OG that will receive {btype}s.', 
        options=[og_name for og_name in OGS_LIST if og_name != og_name_from], on_response=lambda og_name_to: on_resp_og_to(btype, og_name_from, og_name_to))

    async def on_resp_btype(btype):
        await BOT_COMM(id, COMM_CIN, f'Please select the OG that has to give up {btype}s.', options=OGS_LIST, on_response=lambda og_name_from: on_resp_og_from(btype, og_name_from))

    #disallow moving roads
    await BOT_COMM(id, COMM_CIN, 'Please choose a buliding type to move.', options=[btype for btype in B_LIST if btype != B_ROAD], on_response=on_resp_btype)


async def mark_flags_stolen(update, context):
    id = get_chat_id(update)


async def get_scores(update, context):
    id = get_chat_id(update)
    
    all_scores = ''

    for og_name in OGS_LIST:
        all_scores += f'{og_name} has {g_env.OGS[og_name].calculate_points()} point(s).\n'

    await BOT_COMM(id, COMM_COUT, all_scores)

async def view_resources(update, context):
    id = get_chat_id(update)

    msg = "All OG's resources:\n"
    for og_name in OGS_LIST:
        msg += f'{og_name}:\n'
        for r, v in g_env.OGS[og_name]\
            .get_resources()\
            .items():
            msg += f'{r}: {v}\n'
        
        msg += '\n'
    
    await BOT_COMM(id, COMM_COUT, msg)

async def add_misc_points(update, context):
    pass

BOTCOMMANDS_ADMIN = [
    BotCommand('addresource', 'Add a number of resources to an OG.'),
    BotCommand('deleteresource', 'Delete a number of resources to an OG.'),
    BotCommand('movecollateralbuildings', 'Move collateral buildings from one OG to another.'),
    BotCommand('getscores', 'Get scores of all OGs.'),
    BotCommand('viewresources', 'View resources of all OGs.'),
    BotCommand('addmiscpoints', 'Add miscellaneous points to an OG.'),
]

COMMAND_HANDLERS_ADMIN = {
    'addresource': add_resource,
    'deleteresource': delete_resource,
    'movecollateralbuildings': move_collateral_buildings,
    'getscores': get_scores,
    'viewresources': view_resources,
    'addmiscpoints': add_misc_points
}
