import requests
from bs4 import BeautifulSoup
import pandas as pd
import Cities.cities_youla as cities

gorod = ['yakutsk', 'tomsk', 'tyumen', 'omsk', 'moskva', 'sochi', 'krasnodar', 'novosibirsk',
        'kursk', 'sankt-peterburg', 'voronezh', 'ufa']

HOST = 'https://www.youla.ru'
HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
        }

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.findAll('li', class_='product_item')
    ad1 = []

    for item in items:
        ad1.append(
            {
                'title': item.find('a').get('title'),
                'link_product':HOST + item.find('a').get('href'),
                'coast': item.find('div', class_='product_item__description').get_text(strip=True)
            }
        )
    ad =[]
    title, links, coasts = [], [], []

    n = '/' + gorod
    for i in range(len(ad1)):
        if n in ad1[i]['link_product']:
            ad.append(ad1[i])
    
    for i in range(len(ad)):
        title.append(ad[i]['title'])
        links.append(ad[i]['link_product'])
        coasts.append(ad[i]['coast'])

    df = pd.DataFrame()
    df['Название'] = title
    df['Ссылка'] = links
    df['Цена'] = coasts

    writer = pd.ExcelWriter(XLS, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Лист1', index=False)

    writer.sheets['Лист1'].set_column('A:A', 55)
    writer.sheets['Лист1'].set_column('B:B', 50)
    writer.sheets['Лист1'].set_column('C:C', 20)

    writer.save()

for city in gorod:
    XLS = cities.goroda[city]['XLS']
    gorod = cities.goroda[city]['NAME']

    html = get_html(cities.goroda[city]['URL'])
    get_content(html)
