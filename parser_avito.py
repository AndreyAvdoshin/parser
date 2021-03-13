import requests
from bs4 import BeautifulSoup
import csv


CSV = 'avito.csv'
HOST = 'https://www.avito.ru'
URL2 = 'https://www.avito.ru/yakutsk/igry_pristavki_i_programmy/igry_dlya_pristavok-ASgBAgICAUSSAsYJ?cd=1'
URL = 'https://www.avito.ru/yakutsk/igry_pristavki_i_programmy/igry_dlya_pristavok-ASgBAgICAUSSAsYJ?cd=1&s=104'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='iva-item-root-G3n7v')
    ad1 = []

    for item in items:
        ad1.append(
            {
                'title': item.find('a').get('title'),
                'link_product': item.find('a').get('href'),
                'coast': item.find('span', class_='price-text-1HrJ_').get_text(strip=True)
            }
        )
    ad =[]
    n = '/moskva'
    for i in range(len(ad1)):
        if n not in ad1[i]['link_product']:
            ad.append(ad1[i])
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
