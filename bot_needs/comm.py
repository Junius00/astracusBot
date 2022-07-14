from constants.bot.common import COMM_CIN, COMM_COUT
import globals.bot as g_bot
import globals.env as g_env


def get_command(update):
    text = update.message.text
    if not text or text[0] != '/':
        return None

    return text[1:]


def get_chat_id(update):
    return update.message.chat.id


async def BOT_MAP(chat_id, choices=None):
    map_img = g_env.MAP.generate_map_img(choices=choices)
    await g_bot.STATE.send_image(chat_id, map_img)


async def BOT_COMM(chat_id, dir, msg, is_end_of_sequence=True, options=None, on_response=None):
    if dir == COMM_CIN:
        if not on_response:
            raise ValueError("comm CIN requires an on_response callback.")

        async def on_resp(update, context):
            msg_text = update.message.text

            if options and msg_text not in [str(x) for x in options]:
                await g_bot.STATE.send_message(chat_id, 'Invalid input. Please select one of the options and try again.')
                g_bot.STATE.add_pending(chat_id, on_resp)
                await g_bot.STATE.send_message(chat_id, msg, options=options)
                return

            await on_response(msg_text)

        # telegram get input
        g_bot.STATE.mark_busy(chat_id)
        g_bot.STATE.add_pending(chat_id, on_resp)
        await g_bot.STATE.send_message(chat_id, msg, options=options)

    elif dir == COMM_COUT:
        # telegram output
        await g_bot.STATE.send_message(chat_id, msg, clear_pending=is_end_of_sequence)
        if is_end_of_sequence:
            g_bot.STATE.mark_free(chat_id)
            g_bot.STATE.clear_pending(chat_id)
            g_bot.STATE.do_next_action(chat_id)
