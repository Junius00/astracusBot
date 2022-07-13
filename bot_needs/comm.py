from constants.bot.common import COMM_CIN, COMM_COUT
import globals.bot as g_bot

def get_chat_id(update):
    return update.message.chat.id

async def BOT_COMM(chat_id, dir, msg, options=None, on_response=None):
    if dir == COMM_CIN:
        if not on_response:
            raise ValueError("comm CIN requires an on_response callback.")
        
        async def on_resp(update, context):
            msg_text = update.message.text

            if options and msg_text not in [str(x) for x in options]:
                await g_bot.STATE.send_message(chat_id, 'Invalid input. Please select one of the options and try again.')
                g_bot.STATE.modify_pending(chat_id, on_resp)
                await g_bot.STATE.send_message(chat_id, msg, options=options)
                return

            await on_response(msg_text)
        
        #telegram get input
        g_bot.STATE.modify_pending(chat_id, on_resp)
        await g_bot.STATE.send_message(chat_id, msg, options=options)
        
    elif dir == COMM_COUT:
        #telegram output
        await g_bot.STATE.send_message(chat_id, msg)
        g_bot.STATE.clear_pending(chat_id)