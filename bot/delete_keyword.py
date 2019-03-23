from neo4j import GraphDatabase, basic_auth
from telegram.ext.dispatcher import run_async
from credentials.credentials import NEO4J_PASS, NEO4J_CONN, NEO4J_USER
from .neo4j_functions import used_keyword, delete_keyword
KEYWORD_TO_DELETE = 0


@run_async
def delete(bot, update):
    user_id = update.message.chat_id
    bot.sendMessage(chat_id=user_id, text="(You can cancel using /cancel)\n\nGive me the keyword to delete:")
    return KEYWORD_TO_DELETE


@run_async
def keyword_to_delete(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()
    keyword = update.message.text.lower()
    user_id = update.message.chat_id

    if not used_keyword(session, keyword, user_id):
        bot.sendMessage(chat_id=update.message.chat_id, text="You're not using that keyword.")
        session.close()
        return -1

    delete_keyword(session, user_id, keyword)

    bot.sendMessage(chat_id=user_id, text="I won't keep informing you about {}.".format(keyword.title()))

    session.close()
    return -1


@run_async
def cancel(bot, update):
    user_id = update.message.chat_id
    bot.sendMessage(chat_id=user_id, text="Canceled!")
    return -1
