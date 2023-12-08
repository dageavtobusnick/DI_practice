import os
import statistics
import json
from bs4 import BeautifulSoup

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('zip_var_92'))
result_sort = os.path.join(os.path.dirname(__file__), os.path.normpath('result_sorted.json'))
result_filtered = os.path.join(os.path.dirname(__file__), os.path.normpath('result_filtered.json'))
result_charact = os.path.join(os.path.dirname(__file__), os.path.normpath('result_charact.json'))

def read_file(file_name):
    items = []
    with open(file_name, encoding='utf-8') as f:
        str_xml = ''
        lines = f.readlines()
        for line in lines:
            str_xml += line
    
        soup = BeautifulSoup(str_xml, 'xml')
        for cloth in soup.find_all('clothing'):
            item = {}  
            for el in cloth.contents:
                if el.name is None:
                    continue
                elif el.name == 'price' or  el.name == 'reviews':
                    item[el.name] = int(el.get_text().strip())
                elif el.name == 'rating':
                    item[el.name] = float(el.get_text().strip())
                elif el.name == 'new':
                    item[el.name] = el.get_text().strip() == '+'
                elif el.name == 'exclusive' or el.name == 'sporty':
                    item[el.name] = el.get_text().strip() == 'yes'
                else:
                    item[el.name] = el.get_text().strip()
            items.append(item)
    return items


items = []
for i in os.listdir(my_file):
    temp = read_file(os.path.join(my_file, i))
    items += temp

items = sorted(items, key=lambda x: x['price'])

with open(result_sort, 'w', encoding='utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))

filter_views = []
for product in items:
    if product['material'] == "Лен":
        filter_views.append(product)

with open(result_filtered, 'w', encoding='utf-8') as f:
    f.write(json.dumps(filter_views, ensure_ascii=False))

all_rating = {}
color = {'no_size': 0}
all_rating['sum_rating'] = 0
all_rating['min_rating'] = 10 ** 9 + 1
all_rating['max_rating'] = 0
std_rating = [0]
for product in items:
    temp = product['rating']
    all_rating['sum_rating'] += temp
    if all_rating['min_rating'] > temp:
        all_rating['min_rating'] = temp
    if all_rating['max_rating'] < temp:
        all_rating['max_rating'] = temp
    std_rating.append(temp)
    if product.get('size', False) != False:
        if product['size'] in color:
            color[product['size']] += 1
        else:
            color[product['size']] = 1
    else:
        color['no_size'] += 1
all_rating['avr_rating'] = all_rating['sum_rating'] / len(items)
all_rating['std_rating'] = statistics.stdev(std_rating)

all_res = [all_rating, color]

with open(result_charact, 'w', encoding='utf-8') as f:
   f.write(json.dumps(all_res, ensure_ascii=False))