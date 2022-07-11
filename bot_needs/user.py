from constants.bot.users import WHITELIST

def get_user(update):
    return update.message.from_user

def get_identity(user):
    return WHITELIST.get(user.username, None)
