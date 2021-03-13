import requests
from bs4 import BeautifulSoup
import csv


CSV = 'ads.csv'
HOST = 'https://youla.ru/'
URL2 = 'https://youla.ru/yakutsk/hobbi-razvlecheniya/igry-dlya-pristavok-i-pk'
URL = 'https://youla.ru/yakutsk/hobbi-razvlecheniya/igry-dlya-pristavok-i-pk?attributes[term_of_placement][from]=-1%20day&attributes[term_of_placement][to]=now'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('li', class_='product_item')
    ad = []

    for item in items:
        ad.append(
            {
                'title': item.find('a').get('title').strip(),
                'link_product': URL2 + item.find('a').get('href'),
                'coast': item.find('div', class_='product_item__description').get_text(strip=True)
            }
        )
    return ad

def save(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название объявления', 'Ссылка', 'Цена'])
        for item in items:
            writer.writerow([item['title'], item['link_product'], item['coast']])

def parser():
    html = get_html(URL)
    if html.status_code == 200:
        save(get_content(html.text), CSV)
    else:
        print('error')

parser()

