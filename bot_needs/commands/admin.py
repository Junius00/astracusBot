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


async def add_resource(update, context):
    pass

async def delete_resource(update, context):
    pass

async def get_scores(update, context):
    pass

async def view_resources(update, context):
    pass

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
