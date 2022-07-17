import asyncio
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from async_functions.running import synchronous_run

from bot_needs.comm import get_chat_id
import globals.env as g_env


class BotState():
    def __init__(self, app):
        if app is None:
            raise ValueError('Cannot initialise BotState with no application!')

        self.game_is_running = False
        self.admin_ids = []

        self.app = app

        # stores { chat_id: True/False }
        self.is_cancelling = {}

        # stores { chat_id: True/False }
        self.is_busy = {}

        # stores { chat_id: [ action_queue ] }
        self.action_queues = {}

        # stores { chat_id: pending_handler }
        self.pending = {}

    def mark_is_cancelling(self, chat_id, value):
        self.is_cancelling[chat_id] = value

    def check_is_cancelling(self, chat_id):
        return self.is_cancelling.get(chat_id, False)

    def mark_busy(self, chat_id):
        self.is_busy[chat_id] = True

    def mark_free(self, chat_id):
        self.is_busy[chat_id] = False

    def check_busy(self, chat_id):
        return self.is_busy.get(chat_id, False)

    def add_to_action_queue(self, chat_id, action):
        if chat_id not in self.action_queues:
            self.action_queues[chat_id] = []

        self.action_queues[chat_id].append(action)

    def do_next_action(self, chat_id):
        if chat_id in self.action_queues:
            if self.action_queues[chat_id]:
                synchronous_run(self.action_queues[chat_id][0])
                self.action_queues[chat_id] = self.action_queues[chat_id][1:]

            if not self.action_queues[chat_id]:
                del self.action_queues[chat_id]

    def do_all_actions(self):
        for chat_id in self.action_queues.keys():
            if self.check_busy(chat_id):
                continue

            self.do_next_action(chat_id)

    def try_action(self, chat_id, action):
        if self.check_busy(chat_id):
            self.add_to_action_queue(chat_id, action)
        else:
            synchronous_run(action)

    def add_pending(self, chat_id, handler):
        self.pending[chat_id] = handler

    def clear_pending(self, chat_id):
        if chat_id in self.pending:
            del self.pending[chat_id]

    def add_admin_id(self, id):
        self.admin_ids.append(id)

    async def start_game(self):
        if not self.game_is_running:
            self.game_is_running = True
            alert = 'All OGs have logged in. Game has started!'

            await self.alert_all_admins(alert)
            await self.alert_all_ogs(alert)

    async def alert_all_admins(self, msg):
        for id in self.admin_ids:
            await self.send_message(id, msg, clear_pending=False)

    async def alert_all_ogs(self, msg):
        for og in g_env.OGS.values():
            await self.send_message(og.active_id, msg, clear_pending=False)

    async def send_message(self, chat_id, msg, clear_pending=True, options=None):
        if not chat_id:
            print(f'Tried to send:\n{msg} but no chat_id was provided.')
            return

        keys = ReplyKeyboardRemove() if clear_pending else None
        if options:
            keys = ReplyKeyboardMarkup(
                [[KeyboardButton(text)] for text in options])

        await self.app.bot.send_message(chat_id=chat_id, text=msg, reply_markup=keys, read_timeout=10)

    async def send_image(self, chat_id, img_bytes):
        if not chat_id:
            print(f'Tried to send an image but no chat_id was provided.')
            return

        if type(img_bytes) != bytes:
            raise ValueError('image must be in bytes to be displayed.')

        await self.app.bot.send_photo(chat_id, img_bytes)

    async def default_handler(self, update, context):
        await self.send_message(get_chat_id(update), 'We don\'t know what to do with that information. Try a command?')

    def get_handler(self, chat_id):
        return self.pending.get(chat_id, self.default_handler)
