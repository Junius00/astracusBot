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


async def overview(update, context):
    pass

async def buy_building(update, context):
    pass

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
    BotCommand('usepowerupcard', 'Use an unused powerup card.'),
]
COMMAND_HANDLERS_OG = {
    'overview': overview,
    'buybuilding': buy_building,
    'buypowerupcard': buy_powerup_card,
    'viewpowerupcards': view_powerup_cards,
    'usepowerupcard': use_powerup_card
}