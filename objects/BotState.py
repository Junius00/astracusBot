from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from bot_needs.comm import get_chat_id

class BotState():
    def __init__(self, app):
        if app is None:
            raise ValueError('Cannot initialise BotState with no application!')
        
        self.app = app

        #stores { chat_id: pending_handler }
        self.pending = {}
    
    def modify_pending(self, chat_id, handler):
        self.pending[chat_id] = handler
    
    def clear_pending(self, chat_id):
        if chat_id in self.pending:
            del self.pending[chat_id]

    async def send_message(self, chat_id, msg, options=None):
        keys = ReplyKeyboardRemove()
        if options:
            keys = ReplyKeyboardMarkup([[KeyboardButton(text)] for text in options], one_time_keyboard=True)

        await self.app.bot.send_message(chat_id=chat_id, text=msg, reply_markup=keys)

    async def send_image(self, chat_id, img_path):
        with open(img_path, 'rb') as f:
            await self.app.bot.send_photo(chat_id, f)
    
    async def default_handler(self, update, context):
        await self.send_message(get_chat_id(update), 'We don\'t know what to do with that information. Try a command?')

    def get_handler(self, chat_id):
        return self.pending.get(chat_id, self.default_handler)

