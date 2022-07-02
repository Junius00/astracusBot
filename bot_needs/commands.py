import os
import json
from telegram import *
from telegram.ext import *
from constants.names import *
from constants.storage import *
from bot_needs.keyboards import *
import cv2

username_storage = "username_storage.json"
map_location = "assets/current_board.png"

usernames = {}


def reset_usernames():
    return {}

# CONVENIENCE FUNCTIONS


def change_state(update: Update, context: CallbackContext, state: States, new_state):
    state.change_state(new_state)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=TEXTS[new_state], reply_markup=ReplyKeyboardMarkup(KEYBOARDS[new_state]))


def view_usernames():
    filename = os.path.join(FOLDER_DATA, username_storage)
    if os.path.exists(filename):
        f = open(filename, 'r')
        usernames = json.load(f)
        f.close()
    else:
        usernames = reset_usernames()
    return usernames
# COMMON FUNCTIONS


def sign_in(update: Update, context: CallbackContext, state: States):
    username = update.effective_chat.username
    usernames = view_usernames()
    if update.effective_chat.username not in usernames.keys() or usernames[username] != "admin":
        change_state(update, context, state, SIGNUP)
    elif usernames[username] != "admin":
        change_state(update, context, state, USER)
    else:
        change_state(update, context, state, ADMIN)


def sign_up(update: Update, context: CallbackContext, state: States):
    username = update.effective_chat.username
    filename = os.path.join(FOLDER_DATA, username_storage)
    usernames = view_usernames()
    usernames[username] = update.message.text
    with open(filename, 'w') as f:
        json.dump(usernames, f)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"{username} has joined {update.message.text}")
    change_state(update, context, state, USER)


def view_map(update: Update, context: CallbackContext, state: States):
    image = open(map_location, 'rb')
    if image:
        context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=[
                                   InputMediaPhoto(image, caption="Current Map State")])
        context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardMarkup(
            KEYBOARDS[state.current_state]), text=TEXTS[state.current_state])

# USER FUNCTIONS


def buy_building(update: Update, context: CallbackContext, state: States):
    usernames = view_usernames()
    username = update.effective_chat.username
    group = usernames[username]
    state.change_group(group)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Buying building for {group}")
    change_state(update, context, state, NUMBER)

def full_overview(update: Update, context: CallbackContext, state: States):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Giving full overview")
    
def buy_powerup(update: Update, context: CallbackContext, state: States):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Buying powerup")
    
def view_powerups(update: Update, context: CallbackContext, state: States):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Viewing powerups")
    
def use_powerup(update: Update, context: CallbackContext, state: States):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Using powerup")
    
# ADMIN FUNCTIONS

def add_resource(update: Update, context: CallbackContext, state: States):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Adding Resources")
# MISC FUNCTIONS


def group(update: Update, context: CallbackContext, state: States):
    state.change_group(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Selected group is: {update.message.text}")
    change_state(update, context, state, GRID)
    
def number(update: Update, context: CallbackContext, state: States):
    state.change_number(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Selected number is: {update.message.text}")
    change_state(update, context, state, GRID)
    
def grid(update: Update, context: CallbackContext, state: States):
    state.change_grid(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Selected grid is: {update.message.text}")
    change_state(update, context, state, SIDE)
    
def side(update: Update, context: CallbackContext, state: States):
    state.change_side(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Selected side is: {update.message.text}.")
    view_map(update, context, state)
    change_state(update, context, state, USER)
    
def display_map(update: Update, context: CallbackContext, state: States):
    image = open(map_location, 'rb')
    if image:
        context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=[
                                   InputMediaPhoto(image, caption="Current Map State")])
    