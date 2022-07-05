from constants.names import KEY_PUP_ACTION, KEY_PUP_IS_INSTANT
from constants.powerups import PUP_INFO
from bot_needs.comm import BOT_COMM


class Powerup():
    def __init__(self, name):
        self.name = name

        info = PUP_INFO[name]
        self.action = info[KEY_PUP_ACTION]
        self.is_instant = info[KEY_PUP_IS_INSTANT]

    def activate(self, map, og_self, ogs_others):
        self.action(BOT_COMM, map, og_self, ogs_others)