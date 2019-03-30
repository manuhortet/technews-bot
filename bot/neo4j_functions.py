import lang.es as es
import lang.en as en


def create_user(session, user_id, username, lang):
    session.run("CREATE (n:User {{id:'{}', name:'{}', language:'{}'}})".format(user_id, username, lang))


def user_exists(session, user_id):
    user = session.run("OPTIONAL MATCH (n:User {{id: '{}'}}) RETURN n.id as id".format(user_id))
    return True if user.peek().value() else False


def add_keyword(session, user_id, username, keyword):
    session.run("CREATE (n:Keyword {{name:'{}'}})".format(keyword))
    session.run("MATCH (n:User {{id: '{}', name: '{}'}}), (k:Keyword {{name: '{}'}})"
                "CREATE (n)-[r:IS_INTERESTED_IN]->(k)".format(user_id, username, keyword))


def delete_keyword(session, user_id, keyword):
    session.run("MATCH (n:User {{id: '{}'}})-[r:IS_INTERESTED_IN]->(k:Keyword {{name: '{}'}}) DELETE r"
                .format(user_id, keyword))
    session.run("MATCH (k:Keyword) WHERE not (()-[]->(k)) DELETE k;")


def get_keywords(session, user_id, lower):
    keywords = session.run("MATCH (n:User {{id: '{}'}})-[r:IS_INTERESTED_IN]-(k) RETURN k.name AS name".format(user_id))
    names = []
    if keywords.peek():
        for name in keywords.values():
            names.append(name[0].title()) if not lower else names.append(name[0])
        names.sort()
    return names if names else False


def get_lang(session, user_id):
    lang = session.run("MATCH (n:User {{id: '{}'}}) RETURN n.language as lang".format(user_id))
    return es if lang.value()[0] == 'es' else en


# checking if node is empty
def valid_node(node):
    try:
        node.keys()
        return True
    except:
        return False


# checking if keyword is repeated
def used_keyword(session, new_keyword, user_id):
    keywords = session.run("MATCH (:User {{id: '{}'}})-[r]-(k) RETURN k.name as n".format(user_id))
    if keywords.peek():
        for keyword in keywords.values():
            if new_keyword == keyword[0]:
                return True
    return False
