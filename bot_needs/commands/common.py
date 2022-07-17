from telegram import BotCommand, BotCommandScopeChat
from bot_needs.comm import BOT_COMM, BOT_MAP, get_chat_id
from bot_needs.commands.admin import BOTCOMMANDS_ADMIN
from bot_needs.commands.alerts import alerted_map_lock
from bot_needs.commands.og import BOTCOMMANDS_OG
from bot_needs.user import get_identity, get_user
from constants.bot.common import COMM_COUT
from constants.bot.users import ROLE_ADMIN
import globals.bot as g_bot
import globals.env as g_env


async def start_handler(update, context):
    chat_id = get_chat_id(update)
    role = get_identity(get_user(update))

    add_bot_commands = BOTCOMMANDS_ADMIN if role == ROLE_ADMIN else BOTCOMMANDS_OG
    scope = BotCommandScopeChat(chat_id)

    if role != ROLE_ADMIN:
        await g_env.OGS[role].set_active_id(chat_id)
    else:
        g_bot.STATE.add_admin_id(chat_id)

    await g_bot.STATE.app.bot.set_my_commands(BOTCOMMANDS_COMMON + add_bot_commands, scope=scope)
    await g_bot.STATE.send_message(chat_id, f'Welcome to AstracusBot. You are logged in as {role}.')

    not_joined = []

    for og in g_env.OGS.values():
        if not og.active_id:
            not_joined.append(og.name)

    should_start = len(not_joined) == 0

    if should_start:
        await g_bot.STATE.start_game()
    else:
        await g_bot.STATE.send_message(chat_id, f'Please wait for all OGs to join.\nNot joined: {", ".join(not_joined)}')


async def view_map(update, context):
    chat_id = get_chat_id(update)

    if not await alerted_map_lock(chat_id):
        await BOT_MAP(chat_id)

    g_bot.STATE.mark_free(chat_id)


async def cancel_handler(update, context):
    chat_id = get_chat_id(update)
    await g_bot.STATE.call_on_cancel(chat_id)

    g_env.MAP.unlock(chat_id)
    await BOT_COMM(chat_id, COMM_COUT, 'Your last command has been cancelled.' if g_bot.STATE.has_handler(chat_id) else 'There is nothing to cancel at the moment.')


BOTCOMMANDS_COMMON = [
    BotCommand(
        'start', 'Take control of your OG / Sign in as an admin, depending on who you are.'),
    BotCommand('cancel', 'Cancel pending bot commands.'),
    BotCommand('viewmap', 'View the current map.')
]

COMMAND_HANDLERS_COMMON = {
    'start': start_handler,
    'cancel': cancel_handler,
    'viewmap': view_map,
}
