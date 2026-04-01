import requests
import bs4
from fake_headers import Headers
from pprint import pprint
from datetime import datetime
import sys
from fst_logger import logger

keywords = ['Python', 'Программирование', 'Сёма', 
                'Дизайн', 'Нефть', 'Спад', 
                'Принципы', 'SQL', 'GIT', 'GitHub']

@logger
def articles_finder(keywords):
    results = {}

    headers = Headers(browser='opera', os='mac').generate()
    url = 'https://habr.com/ru/articles/'
    response = requests.get(url, headers=headers)

    soup = bs4.BeautifulSoup(response.text, 'lxml') # тут мы получаем структурированный html
    print(f'Ответ страницы: {response.status_code}', end = '\n\n')

    articles = soup.select('div.article-snippet') # тут мы нашли все статьи, с названием, текстом, датой и тд.

    for article in articles:
        title_tag = article.select_one('h2.tm-title.tm-title_h2')
        title = title_tag.text
        
        link_tag = title_tag.select_one('a.tm-title__link')
        link = 'https://habr.com' + link_tag.get('href')
        
        time_tag = article.select_one('time')
        pub_date = time_tag.get('datetime')[:10] 

        for keyword in keywords:
            if keyword.lower() in title.lower():
                results[link] = {'title': title, 
                                'link': link, 
                                'pub_date': pub_date}
                break

        article_response = requests.get(link, headers=headers)
        article_soup = bs4.BeautifulSoup(article_response.text, 'lxml')
        article_tag_text = article_soup.select_one('div.article-formatted-body.article-formatted-body.article-formatted-body_version-2').text

        for keyword in keywords:
            if keyword.lower() in article_tag_text.lower():
                results[link] = {'title': title, 
                                'link': link, 
                                'pub_date': pub_date}
            
    return results

if __name__ == '__main__':
    results = articles_finder(keywords) # здесь я сохранил результат функции
    print(f'Вот 20 самых актуальных новостей на {datetime.now()}', end = '\n\n')
    for result in results.values():
        print(f"Название статьи: {result['title']}.\n", 
              f"Ссылка на статью: {result['link']}.\n",
              f"Дата публикации: {result['pub_date']}", end = '\n\n\n')

        
