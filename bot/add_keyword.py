from neo4j import GraphDatabase, basic_auth
from telegram.ext.dispatcher import run_async
from credentials.credentials import NEO4J_PASS, NEO4J_CONN, NEO4J_USER
from .neo4j_functions import used_keyword, add_keyword, get_lang
KEYWORD_TO_ADD = 0


@run_async
def add(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()

    user_id = update.message.chat_id
    lang = get_lang(session, user_id)

    bot.sendMessage(chat_id=user_id, text=lang.new_keyword)

    return KEYWORD_TO_ADD


@run_async
def keyword_to_add(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()

    user_id = update.message.chat_id
    username = update.effective_user.first_name
    keyword = update.message.text.lower()
    lang = get_lang(session, user_id)

    if used_keyword(session, keyword, user_id):
        bot.sendMessage(chat_id=update.message.chat_id, text=lang.bad_new_keyword)
        session.close()
        return -1

    add_keyword(session, user_id, username, keyword)

    bot.sendMessage(chat_id=user_id, text=lang.add_keyword.success.format(username, keyword.title()))

    session.close()
    return -1


@run_async
def cancel(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()

    user_id = update.message.chat_id
    lang = get_lang(session, user_id)

    bot.sendMessage(chat_id=user_id, text=lang.cancel)

    session.close()
    return -1
