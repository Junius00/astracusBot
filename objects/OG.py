import json
import math
import os
from ast import literal_eval
from bot_needs.comm import BOT_COMM
from constants.bot.common import COMM_COUT
from constants.names import B_HOUSE, B_ROAD, B_VILLAGE, KEY_B, KEY_P, KEY_PUP, KEY_R, R_MINERAL, R_WATER, R_WHEAT, R_WOOD
from constants.og import DOMINANT_RESOURCES, OG_ACTIVE_ID, OG_COLLATERAL, OG_DOMINANT_RESOURCES, OG_FORCE, OG_INSURANCE, OG_MISC, OG_NAME, OG_NO, OG_RMULTIPLIER, OG_USED_POWERUPS, START_C
from constants.powerups import P_NAME
from constants.storage import FOLDER_DATA
from constants.templates import GET_B_TEMPLATE, GET_P_TEMPLATE, GET_R_TEMPLATE
from objects.Building import Building
import globals.env as g_env
import globals.bot as g_bot
from objects.Powerup import Powerup


class OG():
    def __init__(self, name):
        self.name = name
        self.filename = os.path.join(FOLDER_DATA, f'{name}.json')
        self.dominant_r = DOMINANT_RESOURCES[name]
        self.start_c = START_C[name]

        # track which telegram chat is linked to current OG
        self.active_id = None

        # used to increase/decrease resource gain
        self.r_multiplier = 1

        # Barter Trade: force next resource to be this
        self.force_resource = None

        # Insurance: no loss of points from flag stealing
        self.has_insurance = False

        # Just Say No: negate the next targeted action
        self.just_say_no_count = 0

        # Collateral: Fool's Luck Day 3 multiplier
        self.has_collateral_multiplier = False

        # Collateral: store collateral buildings won from other OGs
        self.collateral_buildings = []

        # Count powerups used
        self.used_powerups = 0

        # Count flags lost (for the day)
        self.flags_lost = 0

        # misc points (points excluding number of houses)
        self.misc_points = 0

        self.load_from_json()

    async def set_active_id(self, new_id):
        if self.active_id and self.active_id != new_id:
            if g_bot.STATE.check_busy(self.active_id):
                await BOT_COMM(new_id, COMM_COUT, 'The current OG chat is in the middle of an action. Complete it first, then try and take control again using /start.')
                return

            await BOT_COMM(self.active_id, COMM_COUT, 'You have been deregistered. Please check within your OG to see who took control, or use /start to take control back.')

        self.active_id = new_id

    def reset_items(self):
        self.items = {
            KEY_B: GET_B_TEMPLATE(),
            KEY_R: GET_R_TEMPLATE(),
            KEY_PUP: []
        }

    def set_starting_house(self, house):
        house.owner = self.name
        self.items[KEY_B][B_HOUSE] = [house] + self.items[KEY_B][B_HOUSE]

    def get_starting_building(self):
        houses = self.get_houses()
        villages = self.get_villages()

        if not houses:
            if villages:
                return villages[0]

            return None

        return houses[0]

    def get_building_type(self, btype):
        return self.items[KEY_B][btype]

    def get_houses(self):
        return self.items[KEY_B][B_HOUSE]

    def get_roads(self):
        return self.items[KEY_B][B_ROAD]

    def get_villages(self):
        return self.items[KEY_B][B_VILLAGE]

    def to_obj(self):
        return {
            OG_NAME: self.name,
            OG_DOMINANT_RESOURCES: self.dominant_r,
            OG_ACTIVE_ID: self.active_id,
            OG_RMULTIPLIER: str(self.r_multiplier),
            OG_FORCE: self.force_resource,
            OG_INSURANCE: self.has_insurance,
            OG_NO: str(self.just_say_no_count),
            OG_COLLATERAL: [b.to_obj() for b in self.collateral_buildings],
            OG_USED_POWERUPS: str(self.used_powerups),
            OG_MISC: str(self.misc_points),
            KEY_R: self.items[KEY_R]
        }

    def from_obj(self, obj):
        self.name = obj[OG_NAME]
        self.dominant_r = obj[OG_DOMINANT_RESOURCES]
        self.active_id = obj[OG_ACTIVE_ID]
        self.r_multiplier = literal_eval(obj[OG_RMULTIPLIER])
        self.force_resource = obj[OG_FORCE]
        self.has_insurance = obj[OG_INSURANCE]
        self.just_say_no_count = literal_eval(obj[OG_NO])
        self.collateral_buildings = [Building().from_obj(
            b_obj) for b_obj in obj[OG_COLLATERAL]]
        self.used_powerups = literal_eval(obj[OG_USED_POWERUPS])
        self.misc_points = literal_eval(obj[OG_MISC])
        self.items = {}
        self.items[KEY_R] = obj[KEY_R]
        return self

    def load_from_json(self):
        if os.path.exists(self.filename):
            f = open(self.filename, 'r')
            res = json.load(f)
            f.close()
            og = self.from_obj(res)
            og.items[KEY_B] = {k: [Building().from_obj(b) for b in v]
                               for k, v in res[KEY_B].items()}
            og.items[KEY_PUP] = [Powerup(p[P_NAME]).from_obj(p[P_NAME])
                                 for p in res[KEY_PUP]]
            self = og
            return

        self.reset_items()

    def save_to_json(self):
        obj = self.items.copy()
        savefile = self.to_obj()
        savefile[KEY_B] = {k: [b.to_obj() for b in v]
                           for k, v in obj[KEY_B].items()}
        savefile[KEY_PUP] = [p.to_obj() for p in obj[KEY_PUP]]

        with open(self.filename, 'w') as f:
            json.dump(savefile, f)

    def get_other_r_keys(self):
        return [x for x in [R_WHEAT, R_MINERAL, R_WATER, R_WOOD] if x != self.dominant_r]

    def get_resources(self):
        return self.items[KEY_R]

    def pretty_print_resources(self):
        text = ""
        for resource, value in self.get_resources().items():
            text += f'{resource}: {value}\n'

        return text

    def get_resource_count(self, r_key):
        return self.get_resources()[r_key]

    def add_resource(self, r_key, amount):
        new_amount = amount

        if self.r_multiplier != 1:
            new_amount = math.ceil(amount * self.r_multiplier)
            self.r_multiplier = 1

        if self.flags_lost > 0 and not self.has_insurance:
            new_amount = math.ceil(new_amount * (1 - 0.1 * self.flags_lost))

        self.items[KEY_R][r_key] += new_amount

        return new_amount, new_amount / amount

    def delete_resource(self, r_key, amount):
        cur = self.items[KEY_R][r_key]
        new_amount = cur - amount
        if new_amount < 0:
            new_amount = 0

        self.items[KEY_R][r_key] = new_amount

    # returns True and uses if possible, otherwise False and no change

    def use_resource(self, r_key, amount):
        cur = self.items[KEY_R][r_key]

        if cur < amount:
            return False

        self.items[KEY_R][r_key] -= amount
        return True

    # returns True if possible, otherwise False and no change
    def buy_building(self, building, r_set=None, use_resources=True):
        if use_resources:
            if r_set is None:
                raise ValueError(
                    "r_set must be provided if use_resources is True.")

            old_res = self.items[KEY_R].copy()

            prices = building.get_price_list()
            for p, r in zip(prices, r_set):
                success = self.use_resource(r, p)

                # revert immediately if fail
                if not success:
                    self.items[KEY_R] = old_res
                    return False

        building.owner = self.name
        self.items[KEY_B][building.name].append(building)
        return True

    # returns True if deleted, else False and no change (cannot find building)
    def delete_building(self, building):
        for i, b in enumerate(self.items[KEY_B][building.name]):
            if b.compare(building):
                del self.items[KEY_B][building.name][i]
                return True

        return False

    def calculate_points(self):
        b_points = len(self.items[KEY_B][B_HOUSE]) + \
            3 * len(self.items[KEY_B][B_VILLAGE])
        # is_most_used_powerups = True

        for og_name, og in g_env.OGS.items():
            if og_name == self.name:
                continue

            # if og.used_powerups > self.used_powerups:
                # is_most_used_powerups = False

        # pup_points = 6 if is_most_used_powerups else 0
        pup_points = 0
        return b_points + pup_points + self.misc_points

    def can_say_no(self):
        return self.just_say_no_count > 0

    def say_no(self):
        self.just_say_no_count -= 1

    # returns True is possible, otherwise False and no change
    def buy_powerup(self, pup, r_set):
        old_res = self.items[KEY_R].copy()

        prices = pup.get_price_list()
        for p, r in zip(prices, r_set):
            success = self.use_resource(r, p)

            # revert immediately if fail
            if not success:
                self.items[KEY_R] = old_res
                return False

        if not pup.is_instant:
            self.items[KEY_PUP].append(pup)
            self.items[KEY_PUP] = sorted(
                self.items[KEY_PUP], key=lambda p: p.name)

        return True

    def get_powerups(self):
        return self.items[KEY_PUP]

    def has_powerup(self, pup_name):
        for pup in self.get_powerups():
            if pup.name == pup_name:
                return True

        return False

    async def use_powerup(self, index):
        def on_completion():
            self.used_powerups += 1
            del self.items[KEY_PUP][index]
        await self.get_powerups()[index].activate(self, on_completion)

    def add_collateral_building(self, building):
        building.owner = self.name

        self.collateral_buildings.append(building)
        self.collateral_buildings = sorted(
            self.collateral_buildings, key=lambda b: b.name)

    def count_collateral_buildings(self):
        counts = {
            B_HOUSE: 0,
            B_VILLAGE: 0
        }

        for b in self.collateral_buildings:
            counts[b.name] += 1

        return counts

    def pretty_print_collateral_buildings(self):
        return ', '.join(f'{name}: {count}' for name, count in self.count_collateral_buildings().items())

    def add_flag_lost(self):
        self.flags_lost = min(self.flags_lost + 1, 3)

    def add_misc_points(self, points):
        self.misc_points += points

    def remove_misc_points(self, points):
        self.misc_points -= points
