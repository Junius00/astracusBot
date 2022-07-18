from constants.names import KEY_PUP_ACTION, KEY_PUP_DESC, KEY_PUP_IS_INSTANT, KEY_PUP_QUANTITY, PUP_BARTER_TRADE, PUP_DICE_OF_DESTINY, PUP_FATE_OF_HELL, PUP_FOOLS_LUCK, PUP_INSURANCE, PUP_JUST_SAY_NO, PUP_PAVING_THE_WAY, PUP_POWER_OF_TRADE, PUP_ROAD_BLOCK, PUP_SNEAKY_THIEF, PUP_TELESCOPE
from powerups.actions import barter_trade, randomizer_of_destiny, fate_of_hell, fools_luck, insurance, just_say_no, paving_the_way, power_of_trade, road_block, sneaky_thief, telescope

# Price
PUP_RATIO = (15, [5])


def PUP_INFO():
    return {
        PUP_FOOLS_LUCK: {
            KEY_PUP_QUANTITY: 4,
            KEY_PUP_DESC: 'Earn 50% more resources upon completing a selected game.',
            KEY_PUP_ACTION: fools_luck,
            KEY_PUP_IS_INSTANT: False
        },
        PUP_DICE_OF_DESTINY: {
            KEY_PUP_QUANTITY: 4,
            KEY_PUP_DESC: 'Your tribe will roll an online randomizer between 0 and 50 and you will get that number of resources of your choice.',
            KEY_PUP_ACTION: randomizer_of_destiny,
            KEY_PUP_IS_INSTANT: False
        },
        PUP_POWER_OF_TRADE: {
            KEY_PUP_QUANTITY: 2,
            KEY_PUP_DESC: 'You can trade any number of resources of the same type for the same number of another resource of your choice with Wardin, the mysterious Astracus merchant.',
            KEY_PUP_ACTION: power_of_trade,
            KEY_PUP_IS_INSTANT: False
        },
        PUP_BARTER_TRADE: {
            KEY_PUP_QUANTITY: 4,
            KEY_PUP_DESC: 'You can determine what resource to receive at any station game as the reward.',
            KEY_PUP_ACTION: barter_trade,
            KEY_PUP_IS_INSTANT: False
        },
        PUP_INSURANCE: {
            KEY_PUP_QUANTITY: 2,
            KEY_PUP_DESC: 'You will be immune to the penalties imposed when other tribes steal your flag.',
            KEY_PUP_ACTION: insurance,
            KEY_PUP_IS_INSTANT: True
        },
        PUP_PAVING_THE_WAY: {
            KEY_PUP_QUANTITY: 5,
            KEY_PUP_DESC: 'You can build a road for free.',
            KEY_PUP_ACTION: paving_the_way,
            KEY_PUP_IS_INSTANT: False
        },
        PUP_ROAD_BLOCK: {
            KEY_PUP_QUANTITY: 2,
            KEY_PUP_DESC: 'You can reduce another tribe\'s earnings by 50 percent in the next game that they complete.',
            KEY_PUP_ACTION: road_block,
            KEY_PUP_IS_INSTANT: False
        },
        PUP_SNEAKY_THIEF: {
            KEY_PUP_QUANTITY: 3,
            KEY_PUP_DESC: 'You can steal 25 random resources from another tribe of choice.',
            KEY_PUP_ACTION: sneaky_thief,
            KEY_PUP_IS_INSTANT: True
        },
        PUP_JUST_SAY_NO: {
            KEY_PUP_QUANTITY: 5,
            KEY_PUP_DESC: 'You can now block another tribe\'s action card.',
            KEY_PUP_ACTION: just_say_no,
            KEY_PUP_IS_INSTANT: True
        },
        PUP_FATE_OF_HELL: {
            KEY_PUP_QUANTITY: 3,
            KEY_PUP_DESC: 'You can spin a roulette wheel to decide which opposing tribe to play the action against.',
            KEY_PUP_ACTION: fate_of_hell,
            KEY_PUP_IS_INSTANT: True
        },
        PUP_TELESCOPE: {
            KEY_PUP_QUANTITY: 2,
            KEY_PUP_DESC: 'You can know the identity and number of current points and resources of the leading tribe.',
            KEY_PUP_ACTION: telescope,
            KEY_PUP_IS_INSTANT: False
        }
    }


P_NAME = "pName"
