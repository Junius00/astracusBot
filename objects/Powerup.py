from ast import literal_eval
from calculation.arrays import get_r_paths, ratio_to_price_list
from constants.names import KEY_PUP_ACTION, KEY_PUP_DESC, KEY_PUP_IS_INSTANT
from constants.powerups import P_NAME, PUP_INFO, PUP_RATIO
from bot_needs.comm import BOT_COMM


class Powerup():
    def __init__(self, name):
        self.name = name

        info = PUP_INFO()[name]
        self.ratio = PUP_RATIO
        self.desc = info[KEY_PUP_DESC]
        self.action = info[KEY_PUP_ACTION]
        self.is_instant = info[KEY_PUP_IS_INSTANT]

    def to_obj(self):
        return {
            P_NAME: self.name
        }

    def from_obj(self, obj):
        self.name = obj[P_NAME]
        info = PUP_INFO()[self.name]
        self.ratio = PUP_RATIO
        self.desc = info[KEY_PUP_DESC]
        self.action = info[KEY_PUP_ACTION]
        self.is_instant = info[KEY_PUP_IS_INSTANT]

    def get_price_list(self):
        return ratio_to_price_list(self.ratio)

    def try_build(self, og):
        return get_r_paths(self.ratio, og)

    async def activate(self, og_self):
        await self.action(og_self)
