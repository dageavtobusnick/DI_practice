import os
import json
import msgpack

text_var = 'products_92.json'
my_file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('result.json'))
alt_result = os.path.join(os.path.dirname(__file__), os.path.normpath('alt_result.msgpack'))

with open(my_file) as file:
    data = json.load(file)

def read_data(data):
    result = {}
    for items in data:
        if items['name'] in result:
            result[items['name']].append(items['price'])
        else:
            result[items['name']] = [items['price']]
    return result

def count_info(products):
    result = []
    for item in products:
        avr = sum(products.get(item)) / len(products.get(item))
        minp = min(products.get(item))
        maxp = max(products.get(item))
        result.append({'name': item, 
                               'max': maxp, 
                               'min': minp,
                               'avr': avr})
    return result
products=read_data(data)
products_price=count_info(products)
    
with open(result, 'w') as res:
    res.write(json.dumps(products_price))

with open(alt_result, 'wb') as res:
    res.write(msgpack.dumps(products_price))

print(f'res_json    = {os.path.getsize(result)}')
print(f'res_msgpack = {os.path.getsize(alt_result)}')
print(f'минимум = {min(os.path.getsize(result),os.path.getsize(alt_result))}')