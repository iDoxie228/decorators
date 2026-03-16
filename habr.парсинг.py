import requests
import bs4
from fake_headers import Headers
from pprint import pprint

keywords = ['Python', 'Программирование', 'Сёма', 'Дизайн', 'Нефть', 'Спад', 'Принципы', 'SQL', 'GIT', 'GitGub']
results = []

headers = Headers(browser='opera', os='mac').generate()
url = 'https://habr.com/ru/articles/'
response = requests.get(url)

soup = bs4.BeautifulSoup(response.text, 'lxml') # тут мы получаем структурированный html
print(response.status_code)

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
            results.append({'title': title, 
                            'link': link, 
                            'pub_date': pub_date})
            break
pprint(results)
    
    

    






