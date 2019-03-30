from neo4j import GraphDatabase, basic_auth
from telegram.ext.dispatcher import run_async
from credentials.credentials import NEO4J_PASS, NEO4J_CONN, NEO4J_USER
from .neo4j_functions import used_keyword, delete_keyword, get_lang
KEYWORD_TO_DELETE = 0


@run_async
def delete(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()

    user_id = update.message.chat_id
    lang = get_lang(session, user_id)

    bot.sendMessage(chat_id=user_id, text=lang.delete_keyword)

    session.close()
    return KEYWORD_TO_DELETE


@run_async
def keyword_to_delete(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()

    keyword = update.message.text.lower()
    user_id = update.message.chat_id
    lang = get_lang(session, user_id)

    if not used_keyword(session, keyword, user_id):
        bot.sendMessage(chat_id=update.message.chat_id, text=lang.bad_delete_keyword)
        session.close()
        return -1
    delete_keyword(session, user_id, keyword)

    bot.sendMessage(chat_id=user_id, text=lang.delete_keyword_success.format(keyword.title()))

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
