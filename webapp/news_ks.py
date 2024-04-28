import requests
from bs4 import BeautifulSoup
from datetime import datetime
from webapp.news.models import db, News


def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        print('Доступ запрещен!')
        return False


def get_news_ks():
    html = get_html('https://fksr.org/index.php?page=news&tg=2')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='news noimg4 bg').find_all('li', class_='tp1')
        for news in all_news:
            title = news.find('a', class_='title').text
            url = 'https://fksr.org' + news.find('a', class_='title')['href']
            date = news.find('i').text
            date = datetime.strptime(date, '%d.%m.%Y')
            html_1 = get_html(url)
            if html_1:
                soup_1 = BeautifulSoup(html_1, 'html.parser')
                text = soup_1.find('div', class_='mainblock clearfix').decode_contents()
                path = soup_1.find('div', class_='location').decode_contents()
                text = text.replace(path, '')
            save_news(title, url, date, text)



def save_news(title, url, date, text):
    check_news = News.query.filter(News.url == url).count()
    if not check_news:
        new_news = News(
            title=title,
            url=url,
            date=date,
            text=text,
        )
        db.session.add(new_news)
        db.session.commit()



if __name__ == '__main__':
    print(get_news_ks())
