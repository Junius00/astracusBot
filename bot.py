import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot_needs.comm import BOT_COMM, get_chat_id
from bot_needs.commands.admin import COMMAND_HANDLERS_ADMIN
from bot_needs.commands.common import COMMAND_HANDLERS_COMMON
from bot_needs.commands.og import COMMAND_HANDLERS_OG

from constants.bot.common import COMM_COUT, TOKEN
from constants.bot.users import ROLE_ADMIN, WHITELIST
from constants.names import OG_AVARI, OG_KELGRAS, OG_LEVIATHAN, OG_THERON
from globals.init import init_global, schedule_tasks
import globals.bot as g_bot

async def command_first_pass(command, update, context):
    chat_id = get_chat_id(update)
    if not g_bot.STATE.game_is_running:
        await BOT_COMM(chat_id, COMM_COUT, 'Not all OGs have joined the game. Please wait for the game to start before using any commands.')
        return
    
    await command(update, context)

async def message_handler(update, context):
    chat_id = get_chat_id(update)
    await g_bot.STATE.get_handler(chat_id)(update, context)


def main():
    app = Application.builder().token(TOKEN).build()

    # adding commands for certain whitelisted people
    common = []
    admins = []
    ogs = []

    for username, role in WHITELIST.items():
        if role == ROLE_ADMIN:
            common.append(username)
            admins.append(username)
        elif role in [OG_AVARI, OG_KELGRAS, OG_LEVIATHAN, OG_THERON]:
            common.append(username)
            ogs.append(username)

    for cstr, command in COMMAND_HANDLERS_COMMON.items():
        if cstr == 'start':
            app.add_handler(CommandHandler('start', command, filters=filters.User(username=common)))
            continue

        app.add_handler(CommandHandler(
            cstr, command, filters=filters.User(username=common)))
    for cstr, command in COMMAND_HANDLERS_ADMIN.items():
        app.add_handler(CommandHandler(
            cstr, command, filters=filters.User(username=admins)))
    for cstr, command in COMMAND_HANDLERS_OG.items():
        app.add_handler(CommandHandler(
            cstr, command, filters=filters.User(username=ogs)))

    app.add_handler(MessageHandler(filters.TEXT, message_handler))

    print('Initialsing global variables...')
    init_global(app)
    print('Scheduling tasks...')
    schedule_tasks()
    print('Starting bot polling...')
    app.run_polling()


main()
