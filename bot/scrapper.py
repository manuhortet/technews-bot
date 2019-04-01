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
            link = article['href'].lower()
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
                link = link['href'].lower()
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
                link = link['href'].lower()
            except:
                continue
            if keyword in link:
                links.append("https://www.reuters.com" + link)

    return links


# spanish scrappers
def scrap_bbc_spanish(keywords):
    source = requests.get('https://www.bbc.com/mundo/topics/31684f19-84d6-41f6-b033-7ae08098572a', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.body.find('div', {"class": "column--primary"})
    articles = articles.find_all('div', {"class": "eagle-item faux-block-link"})
    links = []

    for keyword in keywords:
        for article in articles:
            title = article.find('span', {'class': 'title-link__title-text'})
            if keyword in str(title).lower():
                link = article.find('a', {'class': 'title-link'})['href']
                links.append("https://www.bbc.com" + link)

    return links

def scrape_investing_spanish(keywords):
    source = requests.get('https://es.investing.com/news/technology-news', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.body.find('div', {"class": "largeTitle"})
    articles = articles.find_all('article')
    links = []

    for keyword in keywords:
        for article in articles:
            try:
                link = article.find('a', {'class': 'title'})['href'].lower()
            except:
                continue
            if keyword in link:
                links.append("https://es.investing.com" + link)

    return links


def scrape_expansion_spanish(keywords):
    source = requests.get('http://www.expansion.com/empresas/tecnologia.html', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.body.find('div', {"id": "empresastecnologia"})
    articles = articles.find('div', {"class": "fix-c content-items desktop"})
    articles = articles.find('ul', {"class": "auto-items"})
    articles = articles.find_all("li", {"class": "content-item"})
    links = []

    for keyword in keywords:
        for article in articles:
            article_header = article.find('header')
            try:
                title = article_header.find('a')
            except:
                continue
            if keyword in str(title).lower():
                link = title['href'].lower()
                links.append(link)

    return links

def scrape_gizmodo_spanish(keywords):
    source = requests.get('https://es.gizmodo.com/', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.body.find('div', {"class": "page js_page"})
    articles = articles.find_all("article")

    links = []
    for keyword in keywords:
        for article in articles:
            try:
                title = article.find('a', {"class": "js_entry-link"})
            except:
                continue
            if keyword in str(title).lower():
                link = title['href']
                links.append(link)

    return links


def scrape_elpais_spanish(keywords):
    source = requests.get('https://elpais.com/tag/tecnologia/a', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.body.find('div', {"class": "contenedor", "id": "contenedor"})
    articles = articles.find_all("article")
    links = []

    for keyword in keywords:
        for article in articles:
            try:
                article_header = article.find('h2', {"class": "articulo-titulo"})
                title = article_header.find('a')
            except:
                continue
            if keyword in str(title).lower():
                link = title['href']
                links.append("https:" + link)

    return links


def scrape_cnet_spanish(keywords):
    source = requests.get('https://www.cnet.com/es/', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.body.find('div', {"class": "latestScrollItems"})
    articles = articles.find_all("div", {"class": "col-4"})

    links = []
    for keyword in keywords:
        for article in articles:
            try:
                title = article.find('a')
            except:
                continue
            if keyword in str(title).lower():
                link = title['href']
                links.append("https://www.cnet.com" + link)

    return links


def scrape_eleconomista_spanish(keywords):
    source = requests.get('https://www.eleconomista.es/tecnologia/', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.body.find_all("div", {"class": "articleHeadline"})
    links = []

    for keyword in keywords:
        for article in articles:
            try:
                title = article.find('a')
            except:
                continue
            if keyword in str(title).lower():
                link = title['href']
                links.append("https:" + link)

    return links


def scrape_computerhoy_spanish(keywords):
    source = requests.get('https://computerhoy.com/noticias', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.body.find_all("div", {"class": "col-xs-12 col-md-6"})
    links = []

    for keyword in keywords:
        for article in articles:
            try:
                title = article.find('div', {"class": "block-title"})
                title = title.find('a')
            except:
                continue
            if keyword in str(title).lower():
                link = title['href']
                links.append("https://computerhoy.com" + link)

    return links


def scrape_hoy_spanish(keywords):
    source = requests.get('https://www.hoy.es/tecnologia/empresas', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.body.find_all("article")
    links = []

    for keyword in keywords:
        for article in articles:
            try:
                title = article.find('h2')
                title = title.find('a')
            except:
                continue
            if keyword in str(title).lower():
                link = title['href']
                links.append("https://www.hoy.es" + link)

    return links


def scrape_genbeta_spanish(keywords):
    source = requests.get('https://www.genbeta.com/categoria/actualidad', headers=agent).text
    soup = BeautifulSoup(source, 'html.parser')

    articles = soup.body.find_all("article")
    links = []

    for keyword in keywords:
        for article in articles:
            try:
                title = article.find('h2')
                title = title.find('a')
            except:
                continue
            if keyword in str(title).lower():
                link = title['href']
                links.append(link)

    return links


def scrape_news(user_id, lang):
    driver = GraphDatabase.driver(NEO4J_CONN, auth=basic_auth(NEO4J_USER, NEO4J_PASS))
    session = driver.session()

    keywords = get_keywords(session, user_id, lower=True)

    if lang == 'es':
        links = [scrap_bbc_spanish(keywords), scrape_investing_spanish(keywords),
                 scrape_expansion_spanish(keywords), scrape_gizmodo_spanish(keywords),
                 scrape_elpais_spanish(keywords), scrape_cnet_spanish(keywords),
                 scrape_eleconomista_spanish(keywords), scrape_computerhoy_spanish(keywords),
                 scrape_hoy_spanish(keywords), scrape_genbeta_spanish(keywords)]
    else:
        links = [scrap_techcrunch(keywords), scrap_business_insider(keywords), scrap_reuters(keywords)]
    links = list(itertools.chain.from_iterable(links))

    session.close()

    return links
