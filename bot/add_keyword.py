from neo4j import GraphDatabase, basic_auth
from telegram.ext.dispatcher import run_async
from credentials.credentials import NEO4J_PASS, NEO4J_CONN, NEO4J_USER
from .neo4j_functions import used_keyword, add_keyword
KEYWORD_TO_ADD = 0


@run_async
def add(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="(You can cancel using /cancel)\n\nGive me the new keyword:")
    return KEYWORD_TO_ADD


@run_async
def keyword_to_add(bot, update):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()

    user_id = update.message.chat_id
    username = update.effective_user.first_name
    keyword = update.message.text.lower()

    if used_keyword(session, keyword, user_id):
        bot.sendMessage(chat_id=update.message.chat_id, text="You're already using that keyword.")
        session.close()
        return -1

    add_keyword(session, user_id, username, keyword)

    bot.sendMessage(chat_id=user_id, text="Done {}! I'll tell you relevant news about {}."
                    .format(username, keyword.title()))

    session.close()
    return -1


@run_async
def cancel(bot, update):
    user_id = update.message.chat_id
    bot.sendMessage(chat_id=user_id, text="Canceled!")
    return -1
