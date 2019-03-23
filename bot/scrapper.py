import requests
import itertools
from bs4 import BeautifulSoup
from neo4j import GraphDatabase, basic_auth
from credentials.credentials import NEO4J_PASS, NEO4J_CONN, NEO4J_USER
from bot.neo4j_functions import get_keywords

agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/59.0.3071.115 '
                       'Safari/537.36'}


def scrap_techcrunch(keywords):
    source = requests.get('https://techcrunch.com/', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.body.find_all('a')
    links = []

    for keyword in keywords:
        for article in articles:
            link = article['href']
            if keyword in link:
                links.append(link)

    return links


def scrap_business_insider(keywords):
    source = requests.get('https://businessinsider.com/category/tech', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.body.find_all('article')
    links = []

    for keyword in keywords:
        for article in articles:
            link = article.find('a')
            try:
                link = link['href']
            except:
                continue
            if keyword in link:
                links.append(link)

    return links


def scrap_reuters(keywords):
    source = requests.get('https://www.reuters.com/news/technology', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.find_all('article')
    links = []

    for keyword in keywords:
        for article in articles:
            link = article.find('a')
            try:
                link = link['href']
            except:
                continue
            if keyword in link:
                links.append("https://www.reuters.com" + link)

    return links


def scrape_news(user_id):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()

    keywords = get_keywords(session, user_id, lower=True)

    links = [scrap_techcrunch(keywords), scrap_business_insider(keywords), scrap_reuters(keywords)]
    links = list(itertools.chain.from_iterable(links))

    session.close()

    return links
