from constants.bot.common import COMM_CIN, COMM_COUT
from globals.bot import STATE

def get_chat_id(update):
    return update.message.chat.id

async def BOT_COMM(chat_id, dir, msg, options=None, on_response=None):
    if dir == COMM_CIN:
        if not options or not on_response:
            raise ValueError("comm CIN requires an options list and an on_response callback.")
        
        #telegram get input
        STATE.modify_pending(chat_id, lambda update, context: on_response(update.message.chat.text))
        await STATE.send_message(chat_id, msg, options=options)
        
    elif dir == COMM_COUT:
        #telegram output
        await STATE.send_message(chat_id, msg)