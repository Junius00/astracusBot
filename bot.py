import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot_needs.comm import BOT_COMM, get_chat_id, get_command
from bot_needs.commands.admin import COMMAND_HANDLERS_ADMIN
from bot_needs.commands.common import COMMAND_HANDLERS_COMMON
from bot_needs.commands.og import COMMAND_HANDLERS_OG
from calculation.days import get_day

from constants.bot.common import COMM_COUT, TOKEN
from constants.bot.users import ROLE_ADMIN, WHITELIST
from constants.names import OG_AVARI, OG_KELGRAS, OG_LEVIATHAN, OG_THERON
from globals.init import init_global, schedule_tasks
import globals.bot as g_bot
from scheduling.tasks import make_backup


async def command_first_pass(update, context):
    command = get_command(update)
    if not command:
        # cannot extract command
        return

    if command == 'start':
        await COMMAND_HANDLERS_COMMON[command](update, context)
        return

    chat_id = get_chat_id(update)
    if not g_bot.STATE.game_is_running:
        await BOT_COMM(chat_id, COMM_COUT, 'Not all OGs have joined the game. Please wait for the game to start before using any commands.')
        return

    if g_bot.STATE.check_busy(chat_id):
        await BOT_COMM(chat_id, COMM_COUT, 'Maybe finish your current command first before trying another one?', is_end_of_sequence=False)
        return

    # if get_day() == None:
    #     await BOT_COMM(chat_id, COMM_COUT, 'The day is over. You cannot make commands until the next day.', is_end_of_sequence=False)
    #     return

    g_bot.STATE.mark_busy(chat_id)

    make_backup()

    await dict(**COMMAND_HANDLERS_ADMIN, **COMMAND_HANDLERS_COMMON, **COMMAND_HANDLERS_OG)[command](update, context)


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

    for cstr in COMMAND_HANDLERS_COMMON.keys():
        app.add_handler(CommandHandler(cstr, command_first_pass,
                        filters=filters.User(username=common)))
    for cstr in COMMAND_HANDLERS_ADMIN.keys():
        app.add_handler(CommandHandler(cstr, command_first_pass,
                        filters=filters.User(username=admins)))
    for cstr in COMMAND_HANDLERS_OG.keys():
        app.add_handler(CommandHandler(cstr, command_first_pass,
                        filters=filters.User(username=ogs)))

    app.add_handler(MessageHandler(filters.TEXT, message_handler))

    print('Initialsing global variables...')
    init_global(app)
    print('Scheduling tasks...')
    schedule_tasks()
    print('Starting bot polling...')
    app.run_polling()


main()
