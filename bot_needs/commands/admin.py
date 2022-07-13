"""
admin functions:
- add resource of type
- delete resource of type
- get scores
> individual
> everyone
- view resources
> individual
> everyone
- add misc points (e.g. flag stealing)
"""

from telegram import BotCommand
from bot_needs.comm import BOT_COMM, get_chat_id
from constants.bot.common import COMM_CIN, COMM_COUT
from constants.names import OGS_LIST, R_LIST
import globals.env as g_env

async def add_resource(update, context):
    id = get_chat_id(update)

    async def on_resp_number(name, r, count):
        try:
            count = int(count)
        except:
            await BOT_COMM(id, COMM_CIN, 'An invalid amount was entered. Please enter an integer amount (greater than 0) to add.', on_response=lambda count: on_resp_number(name, r, count))
            return

        multi = g_env.OGS[name].r_multiplier
        g_env.OGS[name].add_resource(r, count)
        await BOT_COMM(id, COMM_COUT, f'{count} {r} has been added to {name} ({multi:.1f}x multiplier applied). [New total: {g_env.OGS[name].get_resource_count(r)} {r}]')

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

        g_env.OGS[name].delete_resource(r, count)
        await BOT_COMM(id, COMM_COUT, f'{count} {r} has been removed from {name}. [New total: {g_env.OGS[name].get_resource_count(r)} {r}]')

    async def on_resp_resource(name, r):
        await BOT_COMM(id, COMM_CIN, 'Please enter an integer amount (greater than 0) to remove.', on_response=lambda count: on_resp_number(name, r, count))

    async def on_resp_og(name):
        await BOT_COMM(id, COMM_CIN, 'Please choose a resource to remove.', options=R_LIST, on_response=lambda r: on_resp_resource(name, r))

    await BOT_COMM(id, COMM_CIN, 'Please choose an OG to add resources for.', options=OGS_LIST, on_response=on_resp_og)

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
    BotCommand('viewresources', 'View resources of all OGs.'),
    BotCommand('getscores', 'Get scores of all OGs.'),
    BotCommand('addmiscpoints', 'Add miscellaneous points to an OG.'),
]

COMMAND_HANDLERS_ADMIN = {
    'addresource': add_resource,
    'deleteresource': delete_resource,
    'getscores': get_scores,
    'viewresources': view_resources,
    'addmiscpoints': add_misc_points
}
