from telegram import Update
from telegram.ext import *

from constants.bot import TOKEN

class BotState():
    def __init__(self):
        #stores { chat_id: pending_handler }
        self.pending = {}
    
    def modify_pending(self, chat_id, handler):
        self.pending[chat_id] = handler
    
    def clear_pending(self, chat_id):
        if chat_id in self.pending:
            del self.pending[chat_id]
    
    def default_handler(self, update, context):
        pass

    def get_handler(self, chat_id):
        return self.pending.get(chat_id, self.default_handler)

def message_handler(state, update, context):
    chat_id = update.message.chat.id

    state.get_handler(chat_id)()

def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    state = BotState()
    dispatcher.add_handler(MessageHandler(Filters.text, lambda update, context: message_handler(state, update, context)))

    updater.start_polling()


