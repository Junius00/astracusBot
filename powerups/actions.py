from random import randint
from constants.bot.common import RESP_NO, RESP_YES, COMM_CIN, COMM_COUT
from constants.names import B_HOUSE, B_ROAD, B_VILLAGE, OGS_LIST, PUP_FATE_OF_HELL, PUP_JUST_SAY_NO, PUP_ROAD_BLOCK, PUP_SNEAKY_THIEF, R_LIST

import globals.bot as g_bot
import globals.env as g_env
from objects.Building import Building
from bot_needs.comm import BOT_COMM, BOT_MAP


async def fools_luck_day3(og_self):
    og_self.has_collateral_multiplier = True
    await BOT_COMM(og_self.active_id, COMM_COUT, "You will gain 50% more structures from the amount of collateral the losing tribe has put down, if you win the next mass game.")

async def fools_luck(og_self):
    og_self.r_multiplier = 1.5
    await BOT_COMM(og_self.active_id, COMM_COUT, "Your next station game will yield 50% more resources.")


async def randomizer_of_destiny(og_self):
    dice = randint(0, 50)
    copy_ending = 'ies' if dice != 1 else 'y'

    async def response(r):
        og_self.add_resource(r, dice)
        await BOT_COMM(og_self.active_id, COMM_COUT, f"{dice} cop{copy_ending} of {r} has been added.")

    await BOT_COMM(og_self.active_id, COMM_CIN, f"Please choose a resource type to get {dice} cop{copy_ending} of.", options=R_LIST, on_response=response)


async def power_of_trade(og_self):
    chat_id = og_self.active_id

    async def on_resp_count(rget, rgive, count):
        try:
            count = int(count)
        except:
            await BOT_COMM(chat_id, COMM_CIN, 'Please enter a valid integer.', on_response=lambda c: on_resp_count(rget, rgive, c))
            return

        cur = og_self.get_resource_count(rgive)
        if cur < count:
            await BOT_COMM(chat_id, COMM_COUT, f'You don\'t have enough {rgive} to give. Please try the command again. [Current amount: {cur}]')
            return

        og_self.delete_resource(rgive, count)
        og_self.add_resource(rget, count)

        await BOT_COMM(chat_id, COMM_COUT, f'Successfully traded {count} {rgive} for {count} {rget}!')

    async def on_resp_rgive(rget, rgive):
        if rget == rgive:
            await BOT_COMM(chat_id, COMM_COUT, 'You cannot trade the same resource. Please try the command again.')
            return

        await BOT_COMM(chat_id, COMM_CIN, f'Please enter the amount of {rgive} to give for {rget}.', on_response=lambda count: on_resp_count(rget, rgive, count))

    async def on_resp_rget(rget):
        await BOT_COMM(chat_id, COMM_CIN, f'Please choose a resource to give in return for {rget}.', options=[r for r in R_LIST if r != rget], on_response=lambda rgive: on_resp_rgive(rget, rgive))
    await BOT_COMM(chat_id, COMM_CIN, 'Please choose a resource to receive.', options=R_LIST, on_response=on_resp_rget)


async def barter_trade(og_self):
    chat_id = og_self.active_id

    async def response(r):
        og_self.force_resource = r
        await BOT_COMM(chat_id, COMM_COUT, f'Done! Your next resource gained will be {r}.')

    await BOT_COMM(chat_id, COMM_CIN, 'Please choose a resource to gain as your next station game reward.', options=R_LIST, on_response=response)


async def insurance(og_self):
    og_self.has_insurance = True
    await BOT_COMM(og_self.active_id, COMM_COUT, 'Insurance has been activated! You will no longer lose points from having your flag stolen.')


async def paving_the_way(og_self):
    b = Building()
    b.set_name(B_ROAD)
    b.owner = og_self.name

    choices = g_env.MAP.get_possible_choices(og_self, b)

    async def response(i):
        i = int(i)
        og_self.buy_building(b, use_resources=False)
        g_env.MAP.place_building(choices[i-1], b)
        await BOT_COMM(og_self.active_id, COMM_COUT, 'A road has been placed.')

    await BOT_MAP(og_self.active_id, g_env.MAP.generate_map_img(choices))
    await BOT_COMM(og_self.active_id, COMM_CIN, 'Please choose a road option from the map image.', options=[x + 1 for x in range(len(choices))], on_response=response)

#used if another OG is targeted
async def check_for_just_say_no(og_self, og_target, pup_name, finish_action):
    async def response(res):
        if res == RESP_YES:
            og_target.say_no()
            await BOT_COMM(og_self.active_id, COMM_COUT,
                           f'Oh no! The tribe has activated {PUP_JUST_SAY_NO} against your {pup_name}! Too bad, nothing happened!', is_end_of_sequence=False)
            await BOT_COMM(og_target.active_id, COMM_COUT,
                           f'{PUP_JUST_SAY_NO} is activated. You successfully avoided another tribe\'s action against you! Joke\'s on them!')
        elif res == RESP_NO:
            await BOT_COMM(og_target.active_id, COMM_COUT, f'You have chosen not to use a {PUP_JUST_SAY_NO} card. {pup_name} will be used against you.')
            
            async def continued_action():
                await BOT_COMM(og_self.active_id, COMM_COUT, f'{og_target.name} has decided to not negate your {pup_name} card.', is_end_of_sequence=False)
                await finish_action()

            g_bot.STATE.try_action(og_self.active_id, continued_action)

    if og_target.can_say_no():
        await BOT_COMM(og_self.active_id, COMM_COUT, f'Waiting for {og_target.name} to decide if they want to use {PUP_JUST_SAY_NO}. Please do something else in the meantime.')
        
        async def queue_action():
            await BOT_COMM(
                og_target.active_id, COMM_CIN,
                f"Another OG is trying to use {pup_name} on you. Will you use a '{PUP_JUST_SAY_NO}' Card? ({og_target.just_say_no_count} left)",
                options=[RESP_YES, RESP_NO],
                on_response=response
            )

        g_bot.STATE.try_action(og_target.active_id, queue_action)
        return

    await finish_action()

async def road_block(og_self):
    og_target = sorted([og for og_name, og in g_env.OGS.items() if og_name != og_self.name], key=lambda og: og.calculate_points())[0]

    async def finish_action():
        og_target.r_multiplier = 0.5

        await BOT_COMM(og_self.active_id, COMM_COUT, 'The top OG will have their next earnings halved.')
        await BOT_COMM(og_target.active_id, COMM_COUT, "Because another OG used Road Block, your OG's earnings have been halved for the next game!", is_end_of_sequence=False)

    await check_for_just_say_no(og_self, og_target, PUP_ROAD_BLOCK, finish_action)


async def sneaky_thief(og_self):
    async def on_resp_og_choice(og_name):
        og_target = g_env.OGS[og_name]

        async def finish_action():
            resource = R_LIST[randint(0, 3)]
            count = 0
            while og_target.get_resource_count(resource) < 25 and count < 4:
                resource = R_LIST[randint(0, 3)]
                count += 1
            stolen = min(og_target.get_resource_count(resource), 25)
            og_self.add_resource(resource, stolen)
            og_target.delete_resource(resource, stolen)
            if count > 0:
                await BOT_COMM(og_self.active_id, COMM_COUT, f'{og_target.name} has an insufficient amount of the original resource rolled. We have stolen {stolen} {resource} instead.')
            else:
                await BOT_COMM(og_self.active_id, COMM_COUT, f'You have stolen 25 {resource} from {og_target.name}.')
            await BOT_COMM(og_target.active_id, COMM_COUT, f'Oh no! Another tribe has activated Sneaky Thief. {stolen} {resource} has been stolen from you.', is_end_of_sequence=False)

        await check_for_just_say_no(og_self, og_target, PUP_SNEAKY_THIEF, finish_action)

    await BOT_COMM(og_self.active_id, COMM_CIN, f'You can steal 25 random resources from another tribe of choice.', options=OGS_LIST, on_response=on_resp_og_choice)


async def just_say_no(og_self):
    og_self.just_say_no_count += 1
    await BOT_COMM(og_self.active_id, COMM_COUT, f'You now have {og_self.just_say_no_count} Just Say No card(s).')


async def fate_of_hell(og_self):
    async def on_resp_resource_choice(resource):
        og_target = [og for og_name, og in g_env.OGS.items() if og_name != og_self.name][randint(0, 2)]

        async def finish_action():
            amount = randint(1, 25)
            destroyed = min(og_target.get_resource_count(resource), amount)
            og_target.delete_resource(resource, destroyed)

            await BOT_COMM(og_self.active_id, COMM_COUT, f"Fate of Hell is activated. You have successfully destroyed {destroyed} {resource} from {og_target.name}")
            await BOT_COMM(og_target.active_id, COMM_COUT, f"Oh no! Another tribe has activated the Fate of Hell. {destroyed} {resource} that you own has been destroyed.", is_end_of_sequence=False)

        await check_for_just_say_no(og_self, og_target, PUP_FATE_OF_HELL, finish_action)

    await BOT_COMM(og_self.active_id, COMM_CIN, f'You can choose a resource to destroy from a random tribe. The number will be randomised as well.', options=R_LIST, on_response=on_resp_resource_choice)


async def telescope(og_self):
    og_target = sorted([og for og_name, og in g_env.OGS.items() if og_name != og_self.name], key=lambda og: og.calculate_points())[0]
    resources = og_target.get_resources()
    scores = og_target.calculate_points()
    text = f"Telescope is activated.\n{og_target.name} is leading with {scores} point(s).\nTheir current resources:\n"
    for resource, value in resources.items():
        text += f"{resource}- {value}\n"
    await BOT_COMM(og_self.active_id, COMM_COUT, text)
