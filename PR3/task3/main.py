import os
import statistics
import json
from bs4 import BeautifulSoup

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('zip_var_92'))
result_sort = os.path.join(os.path.dirname(__file__), os.path.normpath('result_sorted.json'))
result_filtered = os.path.join(os.path.dirname(__file__), os.path.normpath('result_filtered.json'))
result_charact = os.path.join(os.path.dirname(__file__), os.path.normpath('result_charact.json'))

def read_file(file_name):
    with open(file_name, encoding='utf-8') as f:
        str_xml = ''
        lines = f.readlines()
        for line in lines:
            str_xml += line
    
        soup = BeautifulSoup(str_xml, 'xml')
        item = {}
        item['name'] = soup.find_all('name')[0].get_text().strip()
        item['const'] = soup.find_all('constellation')[0].get_text().strip()
        item['class'] = soup.find_all('spectral-class')[0].get_text().strip()
        item['radius'] = int(soup.find_all('radius')[0].get_text().strip())
        item['rotation'] = soup.find_all('rotation')[0].get_text().strip()
        item['age'] = soup.find_all('age')[0].get_text().strip()
        item['distance'] = soup.find_all('distance')[0].get_text().strip()
        item['magn'] = soup.find_all('absolute-magnitude')[0].get_text().strip()

        return item


items = []
for i in os.listdir(my_file):
    temp = read_file(os.path.join(my_file, i))
    items.append(temp)

items = sorted(items, key=lambda x: x['radius'])

with open(result_sort, 'w', encoding='utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))

filter_views = []
for star in items:
    if star['const'] == 'Рак':
        filter_views.append(star)

with open(result_filtered, 'w', encoding='utf-8') as f:
    f.write(json.dumps(filter_views, ensure_ascii=False))

all_radius = {}
s_class = {}
all_radius['sum_radius'] = 0
all_radius['min_radius'] = 10 ** 9 + 1
all_radius['max_radius'] = 0
std_radius = [0]
for star in items:
    temp = star['radius']
    all_radius['sum_radius'] += temp
    if all_radius['min_radius'] > temp:
        all_radius['min_radius'] = temp
    if all_radius['max_radius'] < temp:
        all_radius['max_radius'] = temp
    std_radius.append(temp)
    if star['class'] in s_class:
        s_class[star['class']] += 1
    else:
        s_class[star['class']] = 1
all_radius['avr_radius'] = all_radius['sum_radius'] / len(items)
all_radius['std_radius'] = statistics.stdev(std_radius)

all_res = [all_radius, s_class]

with open(result_charact, 'w', encoding='utf-8') as f:
   f.write(json.dumps(all_res, ensure_ascii=False))