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
        str_html = ''
        lines = f.readlines()
        for line in lines:
            str_html += line
    
        soup = BeautifulSoup(str_html, 'html.parser')
        prods = soup.find_all('div', attrs={'class': 'product-item'})

        for prod in prods:
            item = {}            
            item['id'] = prod.a['data-id']
            item['link'] = prod.find_all('a')[1]['href']
            item['img'] = prod.find_all('img')[0]['src']
            item['name'] = prod.find_all('span')[0].get_text().strip()
            item['price'] = int(prod.find_all('price')[0].get_text().replace('₽', '').replace(' ', '').strip())
            item['bonus'] = int(prod.find_all('strong')[0].get_text().replace('+ начислим', '').replace(' бонусов', '').strip())

            props = prod.ul.find_all('li')
            for prop in props:
                item[prop['type']] = prop.get_text().strip()
            items.append(item)
    return items


items = []
for i in os.listdir(my_file):
    temp = read_file(os.path.join(my_file, i))
    items += temp

items = sorted(items, key=lambda x: x['bonus'], reverse=True)

with open(result_sort, 'w', encoding='utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))

filter_views = []
for product in items:
    if product['price'] >= 100000:
        filter_views.append(product)

with open(result_filtered, 'w', encoding='utf-8') as f:
    f.write(json.dumps(filter_views, ensure_ascii=False))

all_bonus = {}
matrix = {'no_matrix': 0}
all_bonus['sum_bonus'] = 0
all_bonus['min_bonus'] = 10 ** 9 + 1
all_bonus['max_bonus'] = 0
std_bonus = [0]
for product in items:
    temp = product['bonus']
    all_bonus['sum_bonus'] += temp
    if all_bonus['min_bonus'] > temp:
        all_bonus['min_bonus'] = temp
    if all_bonus['max_bonus'] < temp:
        all_bonus['max_bonus'] = temp
    std_bonus.append(temp)
    if product.get('matrix', False) != False:
        if product['matrix'] in matrix:
            matrix[product['matrix']] += 1
        else:
            matrix[product['matrix']] = 1
    else:
        matrix['no_matrix'] += 1
all_bonus['avr_bonus'] = all_bonus['sum_bonus'] / len(items)
all_bonus['std_bonus'] = statistics.stdev(std_bonus)

all_res = [all_bonus, matrix]

with open(result_charact, 'w', encoding='utf-8') as f:
   f.write(json.dumps(all_res, ensure_ascii=False))