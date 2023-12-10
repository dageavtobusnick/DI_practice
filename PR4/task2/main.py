import os
import sqlite3
import json

first_file = os.path.join(os.path.dirname(__file__), os.path.normpath('task_1_var_92_item.text'))
second_file = os.path.join(os.path.dirname(__file__), os.path.normpath('task_2_var_92_subitem.json'))
res_file_filter = os.path.join(os.path.dirname(__file__), os.path.normpath('res_filter.json'))
db_file=os.path.join(os.path.dirname(__file__), os.path.normpath('db'))

var=92

def read_first_file():
    data=[]
    with open(first_file,encoding='utf-8') as file:
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

def read_second_file():
    with open(second_file,encoding='utf-8') as file:
        json_string=file.read()
        return json.loads(json_string)

def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def create_first_table(db):
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
    
def create_second_table(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS reviews(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   place_id INTEGER,
   rating REAL,
   convenience INTEGER,
   security INTEGER,
   functionality INTEGER,
   comment TEXT,
   FOREIGN KEY (place_id)  REFERENCES places (id));
""")
    db.commit()

def insert_first_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO places 
        (id, name, street, city, zipcode, floors, year, parking, prob_price, views) 
        VALUES
        (:id, :name, :street, :city, :zipcode, :floors, :year, :parking, :prob_price, :views)""", data)
    db.commit()

def insert_second_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO reviews (place_id, rating, convenience, security, functionality, comment) 
        VALUES(
            (SELECT id FROM places WHERE name = :name),
            :rating, :convenience, :security, :functionality , :comment)""", data)
    db.commit()

def filter_by_rating(db, min_rating):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * 
        FROM places
        WHERE (SELECT AVG(rating) FROM reviews WHERE reviews.place_id==places.id) > ?                
         """, [min_rating])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items  


def charact_security(db,name):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(security) as sum_security,
            AVG(security) as avg_security,
            MIN(security) as min_security, 
            MAX(security) as max_security
        FROM reviews
        WHERE place_id = (SELECT id FROM places WHERE name= ?)                
         """, [name])
    print(dict(res.fetchone()))
    cursor.close()
    return []


def city_popul(db,name):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            *
        FROM places
        JOIN reviews ON places.id = reviews.place_id AND reviews.rating=(SELECT MAX(rating) FROM reviews)
        WHERE name=?
                        """,[name])
    for row in res.fetchall():
        print(dict(row))
    return []



# first_data = read_first_file()
# second_data=read_second_file()
db = connect_to_db(db_file)
# create_first_table(db)
# create_second_table(db)
# insert_first_data(db, first_data)
# insert_second_data(db, second_data)

filtered_places = filter_by_rating(db, 2.6)
with open(res_file_filter, 'w', encoding='utf-8') as f:
    f.write(json.dumps(filtered_places , ensure_ascii=False))

charact_security(db,'Убежище 77')

city_popul(db,"Улей 54")
