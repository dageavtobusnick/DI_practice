import os
import statistics
import json
from bs4 import BeautifulSoup

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('multiple'))
result_sort = os.path.join(os.path.dirname(__file__), os.path.normpath('result_sorted_task2.json'))
result_filtered = os.path.join(os.path.dirname(__file__), os.path.normpath('result_filtered_task2.json'))
result_charact = os.path.join(os.path.dirname(__file__), os.path.normpath('result_charact_task2.json'))

def read_file(file_name):
    items = []
    with open(file_name) as f:
        str_html = ''
        lines = f.readlines()
        for line in lines:
            str_html += line
    
        soup = BeautifulSoup(str_html, 'html.parser')
        prods = soup.find_all('div', attrs={'class': 'col product-specification'})

        for prod in prods:
            item = {}  
            name_tag=prod.find_all('div', attrs={'class': 'product-name'})[0]
            if name_tag != None:
                item['name']=name_tag.find_all('span')[0].get_text()
            table=prod.find_all('table', attrs={'class': 'table table-borderless'})[0]
            for line in table.find_all('tr'):
                split_line=line.find_all('span');
                if split_line[0].get_text()=='Тип:':
                    item['type']=line.find_all('span')[1].get_text()
                if split_line[0].get_text()=='Размер дисплея ("):':
                    item['display_size']=line.find_all('span')[1].get_text()
                if split_line[0].get_text()=='Разрешение экрана:':
                    item['resolution']=line.find_all('span')[1].get_text()
                if split_line[0].get_text()=='Тип процессора:':
                    item['CPU_type']=line.find_all('span')[1].get_text()
                if split_line[0].get_text()=='Размер оперативной памяти (Гб):':
                    item['ram']=int(line.find_all('span')[1].get_text())
            price = prod.find_all('div', attrs={'class': 'price__value'})[0].get_text().split('\xa0')
            price=int(price[0])*1000+int(price[1])
            item['price']=price
            bonus=prod.find_all('span', attrs={'class': 'widget-loyalty__value'})[0].get_text()
            item['bonus']=int(bonus.replace(' ','').replace('+','').replace('\n','').replace('\xa0',''))
            items.append(item)
    return items


items = []
for i in os.listdir(my_file):
    temp = read_file(os.path.join(my_file, i))
    items += temp

items = sorted(items, key=lambda x: x['price'], reverse=True)

with open(result_sort, 'w', encoding='utf-8') as f:
     f.write(json.dumps(items, ensure_ascii=False))

filter_views = []
for product in items:
    if product['ram'] > 8:
        filter_views.append(product)

with open(result_filtered, 'w', encoding='utf-8') as f:
    f.write(json.dumps(filter_views, ensure_ascii=False))

all_bonus = {}
resolution = {'no_resolution': 0}
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
    if product.get('resolution', False) != False:
        if product['resolution'] in resolution:
            resolution[product['resolution']] += 1
        else:
            resolution[product['resolution']] = 1
    else:
        resolution['no_resolution'] += 1
all_bonus['avr_bonus'] = all_bonus['sum_bonus'] / len(items)
all_bonus['std_bonus'] = statistics.stdev(std_bonus)

all_res = [all_bonus, resolution]

with open(result_charact, 'w', encoding='utf-8') as f:
   f.write(json.dumps(all_res, ensure_ascii=False))