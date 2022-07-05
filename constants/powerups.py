from constants.names import KEY_PUP_ACTION, KEY_PUP_IS_INSTANT, KEY_PUP_QUANTITY
from powerups.actions import barter_trade, dice_of_destiny, fate_of_hell, fools_luck, insurance, just_say_no, paving_the_way, power_of_trade, road_block, sneaky_thief, telescope

#Booster Cards
PUP_FOOLS_LUCK = "Fool's Luck"
PUP_DICE_OF_DESTINY = "Dice of Destiny"
PUP_POWER_OF_TRADE = "Power of Trade"
PUP_BARTER_TRADE = "Barter Trade"
PUP_INSURANCE = "Insurance"
PUP_PAVING_THE_WAY = "Paving the Way"

#Action Cards
PUP_ROAD_BLOCK = "Road Block"
PUP_SNEAKY_THIEF = "Sneaky Thief"
PUP_JUST_SAY_NO = "Just Say No"
PUP_FATE_OF_HELL = "Fate of Hell"
PUP_TELESCOPE = "Telescope"

PUP_INFO = {
    PUP_FOOLS_LUCK: {
        KEY_PUP_QUANTITY: 4,
        KEY_PUP_ACTION: fools_luck,
        KEY_PUP_IS_INSTANT: False
    },
    PUP_DICE_OF_DESTINY: {
        KEY_PUP_QUANTITY: 4,
        KEY_PUP_ACTION: dice_of_destiny,
        KEY_PUP_IS_INSTANT: False
    },
    PUP_POWER_OF_TRADE: {
        KEY_PUP_QUANTITY: 2,
        KEY_PUP_ACTION: power_of_trade,
        KEY_PUP_IS_INSTANT: True
    },
    PUP_BARTER_TRADE: {
        KEY_PUP_QUANTITY: 4,
        KEY_PUP_ACTION: barter_trade,
        KEY_PUP_IS_INSTANT: False
    },
    PUP_INSURANCE: {
        KEY_PUP_QUANTITY: 2,
        KEY_PUP_ACTION: insurance,
        KEY_PUP_IS_INSTANT: True
    },
    PUP_PAVING_THE_WAY: {
        KEY_PUP_QUANTITY: 5,
        KEY_PUP_ACTION: paving_the_way,
        KEY_PUP_IS_INSTANT: False
    },
    PUP_ROAD_BLOCK: {
        KEY_PUP_QUANTITY: 2,
        KEY_PUP_ACTION: road_block,
        KEY_PUP_IS_INSTANT: False
    },
    PUP_SNEAKY_THIEF: {
        KEY_PUP_QUANTITY: 3,
        KEY_PUP_ACTION: sneaky_thief,
        KEY_PUP_IS_INSTANT: False
    },
    PUP_JUST_SAY_NO: {
        KEY_PUP_QUANTITY: 5,
        KEY_PUP_ACTION: just_say_no,
        KEY_PUP_IS_INSTANT: False
    },
    PUP_FATE_OF_HELL: {
        KEY_PUP_QUANTITY: 3,
        KEY_PUP_ACTION: fate_of_hell,
        KEY_PUP_IS_INSTANT: False
    },
    PUP_TELESCOPE: {
        KEY_PUP_QUANTITY: 2,
        KEY_PUP_ACTION: telescope,
        KEY_PUP_IS_INSTANT: False
    }
}