from random import randint
from constants.bot.common import RESP_NO, RESP_YES, COMM_CIN, COMM_COUT
from constants.names import B_ROAD, R_LIST

from objects.Building import Building
from bot_needs.comm import BOT_COMM


async def fools_luck(map, og_self, ogs_others):
    og_self.r_multiplier = 1.5
    await BOT_COMM(og_self.active_id, COMM_COUT, "Your next station game will yield 1.5x resources.")

async def dice_of_destiny(map, og_self, ogs_others):
    dice = randint(1, 6)
    copy_ending = 'ies' if dice > 1 else 'y'
    
    async def response(r):
        og_self.add_resource(r, dice)
        await BOT_COMM(og_self.active_id, COMM_COUT, "{dice} cop{copy_ending} of {r} has been added.")
    
    await BOT_COMM(og_self.active_id, COMM_CIN, f"Please choose a resource type to get {dice} cop{copy_ending} of.", options=R_LIST, on_response=response)

async def power_of_trade(map, og_self, ogs_others):
    og_self.has_wardin = True
    await BOT_COMM(og_self.active_id, COMM_COUT, 'Trade with Wardin has been activated. You can now trade 2 of any resource for 1 copy of another.')

async def barter_trade(map, og_self, ogs_others):
    async def response(r):
        og_self.force_resource = r
        await BOT_COMM(og_self.active_id, COMM_COUT, f'Done! Your next resource gained will be {r}.')
    
    await BOT_COMM(og_self.active_id, COMM_CIN, 'Please choose a resource to gain as your next station game reward.', options=R_LIST, on_response=response)

async def insurance(map, og_self, ogs_others):
    og_self.has_insurance = True
    await BOT_COMM(og_self.active_id, COMM_COUT, 'Insurance has been activated! You will no longer lose points from having your flag stolen.')

async def paving_the_way(map, og_self, ogs_others):
    b = Building()
    b.set_name(B_ROAD)
    b.owner = og_self.name

    choices = map.get_possible_choices(og_self, b)
    map.generate_map_img(choices=choices)

    async def response(i):
        og_self.buy_building(b, use_resources=False)
        map.place_building(choices[i-1], b)
        await BOT_COMM(og_self.active_id, COMM_COUT, 'A road has been placed.')

    await BOT_COMM(og_self.active_id, COMM_CIN, 'Please choose a road option from the map image.', options=[x + 1 for x in range(len(choices))], on_response=response)

async def road_block(map, og_self, ogs_others):
    og_target = sorted(ogs_others, key=lambda og: og.calculate_points())[0]
    
    async def finish_action():
        og_target.r_multiplier = 0.5

        await BOT_COMM(og_self.active_id, COMM_COUT, 'The top OG will have their next earnings halved.')
        await BOT_COMM(og_target.active_id, COMM_COUT, "Because another OG used Road Block, your OG's earnings have been halved for the next game!")

    async def response(res):
        if res == RESP_YES:
            BOT_COMM(og_self.active_id, COMM_COUT, '')
        elif res == RESP_NO:
            await finish_action()
    
    if og_target.can_say_no():
        await BOT_COMM(
            og_target.active_id, COMM_COUT, 
            f"Another OG is trying to use Road Block on you. Will you use a 'Just Say No' Card? ({og_target.just_say_no_count} left)",
            options=[RESP_YES, RESP_NO],
            on_response=response
        )

    await finish_action()

async def sneaky_thief(map, og_self, ogs_others):

    pass

async def just_say_no(map, og_self, ogs_others):
    og_self.just_say_no_count += 1
    await BOT_COMM(og_self.active_id, COMM_COUT, f'You now have {og_self.just_say_no_count} cards.')

async def fate_of_hell(map, og_self, ogs_others):
    pass

async def telescope(map, og_self, ogs_others):
    pass