from bot_needs.comm import BOT_COMM
from constants.bot.common import COMM_COUT
import globals.env as g_env

#OG use: not active_id
async def alert_unregistered(chat_id):
    await BOT_COMM(chat_id, COMM_COUT, 'It seems you are not registered as the active chat for your OG. Please use the active chat for your OG, or use /start to take control.')

#will automatically alert if map is in use
async def alerted_map_lock(chat_id):
    if g_env.MAP.is_locked():
        await BOT_COMM(chat_id, COMM_COUT, 'The map is currently in use. Please try again later.')
        return True
    
    return False