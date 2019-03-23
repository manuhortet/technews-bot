# TODO:
# /news
# study where to deploy (dynnos are dying)
# rewrite logs
# MINI improve interactions

import telegram
import logging
import time
from neo4j import GraphDatabase, basic_auth
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater
from telegram.ext.dispatcher import run_async

from credentials.credentials import token, NEO4J_PASS, NEO4J_CONN, NEO4J_USER
from bot.add_keyword import KEYWORD_TO_ADD, cancel, keyword_to_add, add
from bot.delete_keyword import KEYWORD_TO_DELETE, cancel, keyword_to_delete, delete
from bot.neo4j_functions import create_user, user_exist, get_keywords

listening = False

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = telegram.Bot(token=token)


@run_async
def start(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()
    user_id = update.message.chat_id
    username = update.effective_user.first_name
    if user_exist(session, user_id):
        bot.sendMessage(chat_id=user_id, text="Welcome back " + username + "!\n")
        logging.info("Bot running for user with id: {} and name: {}".format(user_id, username))
    else:
        bot.sendMessage(chat_id=user_id, text="Nice to meet you " + username + ".\n")
        create_user(session, user_id, username)
        logging.info("New user created with id: {} and name: {}".format(user_id, username))
    session.close()


@run_async
def keywords(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()
    user_id = update.message.chat_id
    keywords = get_keywords(session, user_id)
    if keywords:
        bot.sendMessage(chat_id=user_id, text="This are the keywords I'm currently using: ")
        bot.sendMessage(chat_id=user_id, text=', '.join(keywords))
    else:
        bot.sendMessage(chat_id=user_id, text="I'm currently not using any keywords! Just napping... zzz")
    session.close()


@run_async
def news(bot, update):
    global listening
    user_id = update.message.chat_id
    bot.sendMessage(chat_id=user_id, text="OK! You'll be receiving news as soon as they appear.")

    listening = True
    while listening:
        start_time = time.time()

        #     get recent news
        #         check if coincidences are still not sent
        #             update sent news and send them

        bot.sendMessage(chat_id=user_id, text="FAKES NEWS.")

        time.sleep(60.0 - ((time.time() - start_time) % 60.0))


@run_async
def stop(bot, update):
    global listening
    bot.sendMessage(chat_id=update.message.chat_id, text="Ok, I'll shut up... :(")
    listening = False
    return -1


def main():
    logging.info("Bot running at @Bamm_bamm_bot")
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    # /start
    dispatcher.add_handler(CommandHandler('start', start))

    # /keywords
    dispatcher.add_handler(CommandHandler('keywords', keywords))

    # /add
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('add', add)],
        states={
            KEYWORD_TO_ADD: [MessageHandler(Filters.text, keyword_to_add)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]))

    # /delete
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('delete', delete)],
        states={
            KEYWORD_TO_DELETE: [MessageHandler(Filters.text, keyword_to_delete)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]))

    # /news
    dispatcher.add_handler(CommandHandler('news', news))

    # /stop
    dispatcher.add_handler(CommandHandler('stop', stop))


    updater.start_polling()
    updater.idle()
