from telegram import *
from telegram.ext import *
from constants.names import *

# COMMON

VIEW_MAP = "View Map"

# ADMIN

ADD_RESOURCE = "Add Resources"
GET_RESOURCE = "Get Resources"
DELETE_RESOURCE = "Delete Resources"
MISC_POINTS = "Miscellaneous Points"
GET_SCORES = "Get Scores"

ADMIN_COMMANDS = [ADD_RESOURCE, GET_RESOURCE,
                  DELETE_RESOURCE, MISC_POINTS, GET_SCORES, VIEW_MAP]

# USER
BUY_BUILDING = "Buy Building"
FULL_OVERVIEW = "Full Overview"
BUY_POWERUP = "Buy Powerup"
VIEW_POWERUP = "View Powerup"
USE_POWERUP = "Use Powerup"

USER_COMMANDS = [BUY_BUILDING, FULL_OVERVIEW,
                 BUY_POWERUP, VIEW_POWERUP, USE_POWERUP, VIEW_MAP]

# STATES

START = "START"
USER = "USER"
ADMIN = "ADMIN"
SIGNUP = "SIGNUP"
GROUP = "GROUP"
NUMBER = "NUMBER"
GRID = "GRID"
SIDE = "SIDE"


class States():
    def __init__(self):
        self.current_state = START
        self.group = OG_AVARI
        self.number = 0
        self.grid = 0
        self.side = 0

    def change_state(self, state):
        self.current_state = state

    def change_group(self, group):
        self.group = group

    def change_number(self, number):
        self.number = number
        
    def change_grid(self, grid):
        self.grid = grid
        
    def change_side(self, side):
        self.side = side


KEYBOARDS = {
    START: [[KeyboardButton(OG_AVARI), KeyboardButton(OG_KELGRAS)], [
        KeyboardButton(OG_LEVIATHAN), KeyboardButton(OG_THERON)]],
    SIGNUP: [[KeyboardButton(OG_AVARI), KeyboardButton(OG_KELGRAS)], [
        KeyboardButton(OG_LEVIATHAN), KeyboardButton(OG_THERON)]],
    GROUP: [[KeyboardButton(OG_AVARI), KeyboardButton(OG_KELGRAS)], [
        KeyboardButton(OG_LEVIATHAN), KeyboardButton(OG_THERON)]],
    USER: [[KeyboardButton(ITEM)] for ITEM in USER_COMMANDS],
    ADMIN: [[KeyboardButton(ITEM)] for ITEM in ADMIN_COMMANDS],
    NUMBER: [[KeyboardButton(5), KeyboardButton(10),
              KeyboardButton(15)],
             [KeyboardButton(20), KeyboardButton(25),
              KeyboardButton(30)],
             [KeyboardButton(35), KeyboardButton(40),
              KeyboardButton(45)],
             [KeyboardButton(50), KeyboardButton(55),
              KeyboardButton(60)]],
    GRID: [[KeyboardButton(1), KeyboardButton(2),
            KeyboardButton(3), KeyboardButton(4)],
           [KeyboardButton(5), KeyboardButton(6),
            KeyboardButton(7), KeyboardButton(8)],
           [KeyboardButton(9), KeyboardButton(10),
            KeyboardButton(11), KeyboardButton(12)],
           [KeyboardButton(13), KeyboardButton(14),
            KeyboardButton(15), KeyboardButton(16)],
           [KeyboardButton(17), KeyboardButton(18),
            KeyboardButton(19), KeyboardButton(20)],
           [KeyboardButton(21), KeyboardButton(22),
            KeyboardButton(23), KeyboardButton(24)],
           [KeyboardButton(25), KeyboardButton(26)], ],
    SIDE: [[KeyboardButton(1), KeyboardButton(2),
            KeyboardButton(3)],
           [KeyboardButton(4), KeyboardButton(5),
            KeyboardButton(6)],
           [KeyboardButton(7), KeyboardButton(8),
            KeyboardButton(9)],
           [KeyboardButton(10), KeyboardButton(11),
            KeyboardButton(12)]],


}

TEXTS = {
    START: "Welcome to Astracus Bot",
    SIGNUP: "Please enter your OG",
    USER: "Please select an action.",
    ADMIN: "Please select an action.",
    GROUP: "Please enter a group.",
    NUMBER: "Please type a number.",
    GRID: "Please enter the grid number.",
    SIDE: "Please enter the side/edge number."
}
