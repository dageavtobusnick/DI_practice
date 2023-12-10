import os
import msgpack
import sqlite3
import csv
import json

data_file = os.path.join(os.path.dirname(__file__), os.path.normpath('task_4_var_92_product_data.msgpack'))
update_file = os.path.join(os.path.dirname(__file__), os.path.normpath('task_4_var_92_update_data.csv'))
res_file_most_update=os.path.join(os.path.dirname(__file__),os.path.normpath("res_most_update.json"))
res_file_res_charact_price= os.path.join(os.path.dirname(__file__),os.path.normpath("res_charact_price.json"))
res_file_res_charact_quantity=os.path.join(os.path.dirname(__file__),os.path.normpath("res_charact_quantity.json"))
res_file_group= os.path.join(os.path.dirname(__file__),os.path.normpath("res_group.json"))
db_file=os.path.join(os.path.dirname(__file__), os.path.normpath('db'))

def read_data_file():
    with open(data_file, 'rb') as file:
        content = file.read()
        data = msgpack.unpackb(content)
    name_set = set()
    items = []
    for i in range(len(data)): 
        if data[i]['name'] not in name_set:
            items.append(data[i])
            name_set.add(data[i]['name'])
    for i in range(len(items)):
        if 'category' in items[i]:
            continue
        else:
            items[i]['category'] = "no"
    return items


def update_data():
    items = []
    with open(update_file, 'r', encoding='utf-8') as file:
        data = csv.reader(file, delimiter=';')
        data.__next__()

        for row in data:
            if len(row) == 0: continue
            item = dict()
            item['name'] = row[0]
            item['method'] = row[1]
            if item['method'] == 'available':
                item['param'] = row[2] == 'True'
            elif item['method'] != 'remove':
                item['param'] = float(row[2]) 
            items.append(item)
    return items


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def create_table(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS product(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT,
   price REAL,
   quantity INTEGER,
   category TEXT,
   fromCity TEXT,
   isAvailable INTEGER,
   views INTEGER,
   version INTEGER);
""")
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO product (name, price, quantity, category, fromCity, isAvailable, views,version) 
        VALUES(:name, :price, :quantity, :category, :fromCity, :isAvailable, :views,0)""", data)
    db.commit()


def delet_name(db, name):
    cursor = db.cursor()
    cursor.execute("DELETE FROM product WHERE name = ?", [name])
    db.commit()


def update_price(db, name, value,command):
    cursor = db.cursor()
    if command=='abs':
        res = cursor.execute('UPDATE product SET price = (price + ?) WHERE (name = ?) AND ((price + ?) > 0)', [value, name, value])
        if res.rowcount > 0:
            cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
            db.commit()
    if command=='percent':
        cursor.execute('UPDATE product SET price = ROUND((price * (1 + ?)), 2) WHERE name = ?', [value, name])
        cursor.execute('UPDATE product SET version = version + 1 WHERE name = ?', [name])
        db.commit()


def update_available(db, name, param):
    cursor = db.cursor()
    cursor.execute("UPDATE product SET isAvailable = ? WHERE (name = ?)", [param, name])
    cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_quantity(db, name, val):
    cursor = db.cursor()
    res = cursor.execute("UPDATE product SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?) > 0)", 
                         [val, name, val])
    if res.rowcount > 0:
        cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def handle_update(db, update_items):
    for item in update_items:
        comands=item['method'].split('_')
        if len(comands)==1:
            if comands[0]=='remove':
                delet_name(db, item['name'])
            else:
                update_available(db, item['name'], item['param'])
        elif comands[0]=='quantity':
            update_quantity(db, item['name'], item['param'])
        else:
            update_price(db, item['name'], item['param'],comands[1])


def top_update(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM product ORDER BY version DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


def charact_price(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            category,
            SUM(price) as sum,
            AVG(price) as avg,
            MIN(price) as min, 
            MAX(price) as max,
            COUNT(*) as total_count
        FROM product
        GROUP BY category
                        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


def charact_quantity(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            category,
            SUM(quantity) as sum,
            AVG(quantity) as avg,
            MIN(quantity) as min, 
            MAX(quantity) as max,
            COUNT(*) as total_count
        FROM product
        GROUP BY category
                        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


def filter_rating(db):
    items = []
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM product
        WHERE isAvailable = 1 AND price>50
        ORDER BY quantity
        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


data = read_data_file()
print(data)
db = connect_to_db(db_file)
create_table(db)
insert_data(db, data)

update = update_data()
handle_update(db, update)

sort_version = top_update(db, 10)
with open(res_file_most_update, 'w', encoding='utf-8') as f:
    f.write(json.dumps(sort_version, ensure_ascii=False))

ch_price = charact_price(db)
with open(res_file_res_charact_price, 'w', encoding='utf-8') as f:
    f.write(json.dumps(ch_price, ensure_ascii=False))

ch_quantity = charact_quantity(db)
with open(res_file_res_charact_quantity, 'w', encoding='utf-8') as f:
    f.write(json.dumps(ch_quantity, ensure_ascii=False))


fil_rat = filter_rating(db)
with open(res_file_group, 'w', encoding='utf-8') as f:
    f.write(json.dumps(fil_rat, ensure_ascii=False))