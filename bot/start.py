import logging
from neo4j import GraphDatabase, basic_auth
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.dispatcher import run_async

import lang.es as es
import lang.en as en
from credentials.credentials import NEO4J_PASS, NEO4J_CONN, NEO4J_USER
from bot.neo4j_functions import create_user, user_exists, get_lang

LANGUAGE = 0


@run_async
def start(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()

    user_id = update.message.chat_id
    user_first_name = update.effective_user.first_name

    # delete user
    session.run("MATCH (n:User {{id: '{}'}})-[r]->(k) DELETE r".format(user_id))
    session.run("MATCH (n:User {{id: '{}'}}) DELETE n".format(user_id))

    if user_exists(session, user_id):
        lang = get_lang(session, user_id)
        bot.sendMessage(chat_id=user_id, text=lang.welcome_back + user_first_name + "! \U0001F496")
    else:
        keyboard = [[InlineKeyboardButton("English", callback_data='en'),
                     InlineKeyboardButton("Spanish", callback_data='es')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=user_id, text='First choose a language:', reply_markup=reply_markup)
        session.close()
        return LANGUAGE

    session.close()
    return -1


@run_async
def language(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()

    user_id = update.callback_query.message.chat_id
    user_first_name = update.effective_user.first_name
    lang = es if update.callback_query.data == 'es' else en

    create_user(session, user_id, user_first_name, update.callback_query.data)
    bot.sendMessage(chat_id=user_id, text=lang.nice_to_meet_you + user_first_name + ". \U0001F601")
    bot.sendMessage(chat_id=user_id, text=lang.intro_msg)
    logging.info("NEW USER: {}, {}, @{}".format(user_id, user_first_name, update.effective_user.username))

    session.close()
    return -1


@run_async
def cancel(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()

    user_id = update.message.chat_id
    lang = get_lang(session, user_id)

    bot.sendMessage(chat_id=user_id, text=lang.cancel)

    session.clsoe()
    return -1
