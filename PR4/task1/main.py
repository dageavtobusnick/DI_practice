import os
import sqlite3
import json

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('task_1_var_92_item.text'))
res_file_sorted = os.path.join(os.path.dirname(__file__), os.path.normpath('res_sort.json'))
res_file_filter = os.path.join(os.path.dirname(__file__), os.path.normpath('res_filter.json'))
db_file=os.path.join(os.path.dirname(__file__), os.path.normpath('first'))

var=92

def read_file():
    data=[]
    with open(my_file,encoding='utf-8') as file:
        lines = file.readlines()
        item={}
        for line in lines:
            value=str(line).split(':')
            if line == "=====\n":
                data.append(item)
                item={}
                continue
            clered_value=value[2].replace('\n','')
            if not value[0] in('name','street','city'):
                if not value[0] in('parking'):
                    item[value[0]]=int(clered_value)
                else:
                    item[value[0]]=bool(clered_value)
            else:
                item[value[0]]=clered_value
                
    return data


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def create_table(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS places(
   id INT PRIMARY KEY,
   name TEXT,
   street TEXT,
   city TEXT,
   zipcode INTEGER,
   floors INTEGER,
   year INTEGER,
   parking INTEGER,
   prob_price INTEGER,
   views INTEGER);
""")
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO places 
        (id, name, street, city, zipcode, floors, year, parking, prob_price, views) 
        VALUES
        (:id, :name, :street, :city, :zipcode, :floors, :year, :parking, :prob_price, :views)""", data)
    db.commit()



def sort_by_years(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM places ORDER BY year DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


def charact_views(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(views) as sum,
            AVG(views) as avg,
            MIN(views) as min, 
            MAX(views) as max
        FROM places
                        """)
    print(dict(res.fetchone()))
    cursor.close()
    return []


def city_popul(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM places) as count,
            city
        FROM places
        GROUP BY city
                        """)
    for row in res.fetchall():
        print(dict(row))
    return []


def filter_prob_price(db, min_prob_price, limit):
    items = []
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM places
        WHERE prob_price >= ?
        ORDER BY views DESC
        LIMIT ?
        """, [min_prob_price, limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# data = read_file()

db = connect_to_db(db_file)
# create_table(db)
# insert_data(db, data)

sort_views = sort_by_years(db, var+10)
with open(res_file_sorted, 'w', encoding='utf-8') as f:
    f.write(json.dumps(sort_views, ensure_ascii=False))

charact_views(db)

city_popul(db)


fil_rat = filter_prob_price(db, 500000000, var+10)
with open(res_file_filter, 'w', encoding='utf-8') as f:
    f.write(json.dumps(fil_rat, ensure_ascii=False))
