import os
import statistics
import json
from bs4 import BeautifulSoup

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('single'))
result_sort = os.path.join(os.path.dirname(__file__), os.path.normpath('result_sorted_task1.json'))
result_filtered = os.path.join(os.path.dirname(__file__), os.path.normpath('result_filtered_task1.json'))
result_charact = os.path.join(os.path.dirname(__file__), os.path.normpath('result_charact_task1.json'))

def read_file(file_name):
    item = {}
    with open(file_name) as f:
        str_html = ''
        lines = f.readlines()
        for line in lines:
            str_html += line
        soup = BeautifulSoup(str_html, 'html.parser')
        prods = soup.find_all('div', attrs={'class': 'params-list__item'})
        price = soup.find_all('div', attrs={'class': 'product-price__current'})[0].get_text().split('\xa0')
        price=int(price[0])*1000+int(price[1])
        item['price']=price
        for prod in prods:
            name=prod.find_all('div',attrs={'class': 'params-list__item-name'})[0].get_text().strip().replace('\xa0','');
            values=prod.find_all('div',attrs={'class': 'params-list__item-value'})[0].find_all('span')
            if(values):
                value=values[0].get_text()
                if name=="Тип":
                    item['type']=value
                if name=="Дисплей":
                    item['display']=value
                if name=="Размер дисплея (\")":
                    item['display_size']=value
                if name=="Разрешение экрана":
                    item['resolution']=value
                if name=="Поверхность экрана":
                    item['surface']=value
                if name=="Тип процессора":
                    item['CPU']=value
                if name=="Серия процессора":
                    item['CPU_series']=value
                if name=="Количество ядер процессора":
                    item['cores_number']=int(value)
                if name=="Частота процессора (МГц)":
                    item['CPU_frequency']=value
                if name=="Размер оперативной памяти (Гб)":
                    item['ram']=int(value)
                if name=="Тип жесткого диска":
                    item['disk_type']=value
                if name=="Объем жесткого диска (Гб)":
                    item['disk_size']=int(value)
                if name=="Модель видеокарты":
                    item['cart_type']=value
                if name=="Аккумулятор (время работы)":
                    item['battery_time']=value
                if name=="Операционная система":
                    item['os']=value
                if name=="Габариты (ВxШxГ) (см)":
                    item['size']=value
                if name=="Вес (кг)":
                    item['mass']=float(value)
                if name=="Страна-производитель":
                    item['country']=value
    return item


items = []
for i in os.listdir(my_file):
    temp = read_file(os.path.join(my_file, i))
    items.append(temp)

items = sorted(items, key=lambda x: x['cores_number'], reverse=True)

with open(result_sort, 'w', encoding='utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))

filter_views = []
for product in items:
    if 'surface' in product.keys() and product['surface'] == "глянцевая":
        filter_views.append(product)

with open(result_filtered, 'w', encoding='utf-8') as f:
    f.write(json.dumps(filter_views, ensure_ascii=False))

all_price = {}
os = {'no_os': 0}
all_price['sum_price'] = 0
all_price['min_price'] = 10 ** 9 + 1
all_price['max_price'] = 0
std_price = [0]
for product in items:
    temp = product['price']
    all_price['sum_price'] += temp
    if all_price['min_price'] > temp:
        all_price['min_price'] = temp
    if all_price['max_price'] < temp:
        all_price['max_price'] = temp
    std_price.append(temp)
    if product.get('os', False) != False:
        if product['os'] in os:
            os[product['os']] += 1
        else:
            os[product['os']] = 1
    else:
        os['no_os'] += 1
all_price['avr_price'] = all_price['sum_price'] / len(items)
all_price['std_price'] = statistics.stdev(std_price)

all_res = [all_price, os]

with open(result_charact, 'w', encoding='utf-8') as f:
   f.write(json.dumps(all_res, ensure_ascii=False))