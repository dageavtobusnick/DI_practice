import os
import re
import statistics
import json
from bs4 import BeautifulSoup

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('zip_var_92'))
result_sort = os.path.join(os.path.dirname(__file__), os.path.normpath('result_sorted.json'))
result_filtered = os.path.join(os.path.dirname(__file__), os.path.normpath('result_filtered.json'))
result_charact = os.path.join(os.path.dirname(__file__), os.path.normpath('result_charact.json'))

def file_read(file_name):
    with open(file_name, encoding='utf-8') as f:
        str_html = ''
        lines = f.readlines()
        for line in lines:
            str_html += line
    
        soup = BeautifulSoup(str_html, 'html.parser')

        item = {}
        item['city'] = soup.find_all('span', string=re.compile("Город"))[0].get_text().split(':')[1].strip()
        item['name'] = soup.find_all('h1')[0].get_text().split(':')[1].strip()
        address = soup.find_all('p')[0].get_text()
        ind = address.find('Индекс')
        item["street"] = address[:ind].split(':')[1].strip()
        item["index"] = int(address[ind:].split(':')[1].strip())
        item['floor'] = int(soup.find_all('span', attrs={"class": 'floors'})[0].get_text().split(':')[1].strip())
        item['year'] = int(soup.find_all('span', attrs={"class": 'year'})[0].get_text().split(" в ")[1].strip())
        item['parking'] = bool(soup.find_all('span', string=re.compile("Парковка"))[0].get_text().split(':')[1].strip())
        item['img'] = soup.find_all('img')[0]['src']
        item['rating'] = float(soup.find_all('span', string=re.compile("Рейтинг"))[0].get_text().split(':')[1].strip())
        item['views'] = int(soup.find_all('span', string=re.compile("Просмотры"))[0].get_text().split(':')[1].strip())
        
        return item


items = []
for i in os.listdir(my_file):
    temp = file_read(os.path.join(my_file, i))
    items.append(temp)

items = sorted(items, key=lambda x: x['views'], reverse=True)

with open(result_sort, 'w', encoding='utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))


filter_views = []
for place in items:
    if place['rating'] >= 4:
        filter_views.append(place)

with open(result_filtered, 'w', encoding='utf-8') as f:
    f.write(json.dumps(filter_views, ensure_ascii=False))


all_views = {}
cities = {}
all_views['sum_views'] = 0
all_views['min_views'] = 10 ** 9 + 1
all_views['max_views'] = 0
std_views = [0]
for place in items:
     temp = place['views']
     all_views['sum_views'] += temp
     if all_views['min_views'] > temp:
         all_views['min_views'] = temp
     if all_views['max_views'] < temp:
         all_views['max_views'] = temp
     std_views.append(temp)
     if place['city'] in cities:
         cities[place['city']] += 1
     else:
         cities[place['city']] = 1
all_views['avr_views'] = all_views['sum_views'] / len(items)
all_views['std_views'] = statistics.stdev(std_views)

all_res = [all_views, cities]

with open(result_charact, 'w', encoding='utf-8') as f:
    f.write(json.dumps(all_res, ensure_ascii=False))