from bot_stuff.credentials import BOT_TOKEN, BOT_USERNAME
from flask import Flask, request
import re
import requests
import telegram
from bot_needs.commands import *

bot = telegram.Bot(token=BOT_TOKEN)
app = Flask(__name__)

URL = ""


@app.route('/', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    text = update.message.text.encode('utf-8').decode()

    if text == "/start":
        bot_welcome = f"""
       Hi. I am {BOT_USERNAME}. Nice to meet you.
       """
        bot.sendMessage(chat_id=chat_id, text=bot_welcome,
                        reply_to_message_id=msg_id)

    else:
        try:
            text = re.sub(r"\W", "_", text)

            url = "https://api.adorable.io/avatars/285/{}.png".format(
                text.strip())

            bot.sendPhoto(chat_id=chat_id, photo=url,
                          reply_to_message_id=msg_id)
        except Exception:
            bot.sendMessage(
                chat_id=chat_id, text="I do not understand. Can you not be stupid?", reply_to_message_id=msg_id)

    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={URL}")
    # something to let us know things work
    if s:
        return "ok"
    else:
        return "no"


if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)
