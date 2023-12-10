import os
import sqlite3
import json
import pickle

my_file_part_1 = os.path.join(os.path.dirname(__file__), os.path.normpath('task_3_var_92_part_1.json'))
my_file_part_2 = os.path.join(os.path.dirname(__file__), os.path.normpath('task_3_var_92_part_2.pkl'))
res_file_sorted = os.path.join(os.path.dirname(__file__), os.path.normpath('res_sorted.json'))
res_file_popul_genre = os.path.join(os.path.dirname(__file__), os.path.normpath("res_popul_genre.json"))
res_file_filtrer = os.path.join(os.path.dirname(__file__), os.path.normpath("res_filtrer.json"))
db_file=os.path.join(os.path.dirname(__file__), os.path.normpath('db'))

var=92

def read_second(file_name):
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
    for item in data:
        item.pop('acousticness')
        item.pop('energy')
    return data


def read_first(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data=json.loads(file.read())
        for item in data:
            item.pop('explicit')
            item.pop('danceability')
        return data


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def create_table(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS music(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   artist TEXT,
   song TEXT,
   duration_ms INTEGER,
   year INTEGER,
   tempo REAL,
   genre TEXT,
   popularity INTEGER);
""")
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO music (artist, song, duration_ms, year, tempo, genre, popularity) 
        VALUES(:artist, :song, :duration_ms, :year, :tempo, :genre, :popularity)""", data)
    db.commit()


def top_duration_ms(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM music ORDER BY duration_ms DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


def charact_popularity(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(popularity) as sum,
            AVG(popularity) as avg,
            MIN(popularity) as min, 
            MAX(popularity) as max
        FROM music
                        """)
    print(dict(res.fetchone()))
    cursor.close()
    return []


def popul_genre(db):
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
        SELECT 
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM music) as count,
            genre
        FROM music
        GROUP BY genre
                        """)
    for row in res.fetchall():
        items.append(dict(row))
        print(dict(row))
    return items


def filter_year(db, min_pop, limit):
    items = []
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM music
        WHERE popularity >= ?
        ORDER BY year DESC
        LIMIT ?
        """, [min_pop, limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# data_1 = read_first(my_file_part_1)
# data_2 = read_second(my_file_part_2)
# data12 = data_1 + data_2

db = connect_to_db(db_file)
# create_table(db)
# insert_data(db, data12)

sort_duration_ms = top_duration_ms(db, var+10)
with open(res_file_sorted, 'w', encoding='utf-8') as f:
    f.write(json.dumps(sort_duration_ms, ensure_ascii=False))

charact_popularity(db)

pop_genre = popul_genre(db)
with open(res_file_popul_genre, 'w', encoding='utf-8') as f:
    f.write(json.dumps(pop_genre, ensure_ascii=False))

fil_pop = filter_year(db, 85, var+15)
with open(res_file_filtrer, 'w', encoding='utf-8') as f:
    f.write(json.dumps(fil_pop, ensure_ascii=False))