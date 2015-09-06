import logging
import telegram
from stipuha_user_handler import *

__author__ = 'vovapolu'

LAST_UPDATE_ID = None
usersHandlers = dict()

def main():
    global LAST_UPDATE_ID

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Telegram Bot Authorization Token
    bot = telegram.Bot('139303220:AAEVttjtRpho0CocNEgoEhsE0sE6UVS30Ck')

    # This will be our global variable to keep the latest update_id when requesting
    # for updates. It starts with the latest update_id if available.
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while True:
        run(bot)


def run(bot):
    global LAST_UPDATE_ID
    global usersHandlers

    StipuhaUser.write_users_to_disk(StipuhaUser.FILE)

    # Request updates after the last updated_id
    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
        # chat_id is required to reply any message
        chat_id = str(update.message.chat_id)
        message = update.message.text.encode('utf-8')

        if message:
            # Reply the message
            if chat_id not in usersHandlers:
                usersHandlers[chat_id] = StipuhaUserHandler(bot, chat_id)
            usersHandlers[chat_id].receive_message(message)

            # Updates global offset to get the new updates
            LAST_UPDATE_ID = update.update_id + 1


if __name__ == '__main__':
    main()