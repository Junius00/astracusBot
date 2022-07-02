from telegram import *
from telegram.ext import *
from requests import *
from bot_needs.commands import *
from bot_needs.keyboards import *

'''
[...] comments are mine
- sign in:
> let users sign in/register to be admin (proggies) or users (OGs)

common functions:
- view full map

admin functions:
- add resource of type
- delete resource of type
- get scores
> individual
> everyone
- view resources
> individual
> everyone
- add misc points (e.g. flag stealing)

user functions:
- view full overview
> full resources count
> score count
- buy a building
- buy a powerup card
- view powerup cards
- use powerup cards

bot should also notify users on events (e.g. power up used against them)
'''

updater = Updater(token="5388615241:AAHZGvOPksoEUU-R05wT70ef-OvIn30CvUo")
dispatcher = updater.dispatcher

state = States()


def startCommand(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hi! Astracus bot is here!")
    sign_in(update, context, state)


def messageHandler(update: Update, context: CallbackContext):
    # WITHOUT ADDITIONAL STUFF
    if state.current_state == START:
        sign_in(update, context, state)
    elif state.current_state == SIGNUP:
        sign_up(update, context, state)
    # JUST UPDATE STATE
    elif state.current_state == GROUP:
        group(update, context, state)
    elif state.current_state == NUMBER:
        number(update, context, state)
    elif state.current_state == GRID:
        grid(update, context, state)
    elif state.current_state == SIDE:
        side(update, context, state)
    # NEED MULTIPLE IF STATEMENTS
    elif state.current_state == USER:
        text = update.message.text
        if text == BUY_BUILDING:
            buy_building(update, context, state)
    elif state.current_state == ADMIN:
        view_map(update, context, state)
        state.change_state(SIGNUP)


def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

    global likes, dislikes

    if "like" in query:
        likes += 1

    if "dislike" in query:
        dislikes += 1

    print(f"likes => {likes} and dislikes => {dislikes}")


dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
dispatcher.add_handler(CallbackQueryHandler(queryHandler))

updater.start_polling()
