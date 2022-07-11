from telegram import BotCommand, BotCommandScopeChat
from bot_needs.comm import get_chat_id
from bot_needs.commands.admin import BOTCOMMANDS_ADMIN
from bot_needs.commands.og import BOTCOMMANDS_OG
from bot_needs.user import get_identity, get_user
from constants.bot.users import ROLE_ADMIN
import globals.bot as g_bot
import globals.env as g_env

async def start_handler(update, context):
    chat_id = get_chat_id(update)
    role = get_identity(get_user(update))

    add_bot_commands = BOTCOMMANDS_ADMIN if role == ROLE_ADMIN else BOTCOMMANDS_OG
    scope = BotCommandScopeChat(chat_id)

    await g_bot.STATE.app.bot.set_my_commands(BOTCOMMANDS_COMMON + add_bot_commands, scope=scope)
    await g_bot.STATE.send_message(chat_id, f'Welcome to AstracusBot. You are logged in as {role}. Please select a command to continue.')
    
async def view_map(update, context):
    pass

BOTCOMMANDS_COMMON = [
    BotCommand('viewmap', 'View the current map.')
]

COMMAND_HANDLERS_COMMON = {
    'start': start_handler,
    'viewmap': view_map
}