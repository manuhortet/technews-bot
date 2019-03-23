# TODO:
# study where to deploy (dynnos are dying)
# refactor sources

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
from bot.scrapper import scrape_news

listening = False

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = telegram.Bot(token=token)


@run_async
def start(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()

    user_id = update.message.chat_id
    user_first_name = update.effective_user.first_name

    if user_exist(session, user_id):
        bot.sendMessage(chat_id=user_id, text="Welcome back " + user_first_name + "! \U0001F496")
    else:
        bot.sendMessage(chat_id=user_id, text="Nice to meet you " + user_first_name + ". \U0001F601")
        bot.sendMessage(chat_id=user_id, text="You can tell me some keywords you want to be informed about using the command /add. Try it!")
        create_user(session, user_id, user_first_name)
        logging.info("NEW USER: {}, {}, {}".format(user_id,
                                                   user_first_name,
                                                   update.effective_user.username))

    session.close()


@run_async
def keywords(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()
    user_id = update.message.chat_id
    keywords = get_keywords(session, user_id, lower=False)
    if keywords:
        bot.sendMessage(chat_id=user_id, text="This are the keywords I'm currently using: ")
        bot.sendMessage(chat_id=user_id, text=', '.join(keywords))
    else:
        bot.sendMessage(chat_id=user_id, text="I'm currently not using any keywords! Just napping... \U0001F634")
    session.close()


@run_async
def news(bot, update):
    global listening
    user_id = update.message.chat_id
    bot.sendMessage(chat_id=user_id, text="OK! You'll be receiving news as soon as they appear. \U0001F47C\U0001F4E1")

    sent_links = []
    listening = True
    while listening:
        logging.info('Scrapping for {}, {}, {}'.format(user_id,
                                                       update.effective_user.first_name,
                                                       update.effective_user.username))
        message_counter = 0
        start_time = time.time()
        new_links = scrape_news(user_id)
        for link in new_links:
            if message_counter > 2:
                break
            if link not in sent_links:
                bot.sendMessage(chat_id=user_id, text=link)
                message_counter +=1
                sent_links.append(link)

        time.sleep(60.0 - ((time.time() - start_time) % 60.0))


@run_async
def stop(bot, update):
    global listening
    bot.sendMessage(chat_id=update.message.chat_id, text="Ok... \U0001F636")
    listening = False
    return -1


def main():
    logging.info("Bot running at @Bamm_bamm_bot")
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('keywords', keywords))
    dispatcher.add_handler(CommandHandler('news', news))
    dispatcher.add_handler(CommandHandler('stop', stop))

    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('add', add)],
        states={
            KEYWORD_TO_ADD: [MessageHandler(Filters.text, keyword_to_add)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]))

    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('delete', delete)],
        states={
            KEYWORD_TO_DELETE: [MessageHandler(Filters.text, keyword_to_delete)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]))

    updater.start_polling()
    updater.idle()
