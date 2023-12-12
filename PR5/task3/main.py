import msgpack
import csv
import os
import pickle
from pymongo import MongoClient

data_file_pkl = os.path.join(os.path.dirname(__file__), os.path.normpath('task_1_item.pkl'))
data_file_csv = os.path.join(os.path.dirname(__file__), os.path.normpath('task_2_item.csv'))
data_file_msgpack = os.path.join(os.path.dirname(__file__), os.path.normpath('task_3_item.msgpack'))

def connect():
    client = MongoClient()
    db = client["database-1"]
    return db.person_data

def open_pkl(file_pkl):
    with open(file_pkl, "rb") as file:
        res = pickle.load(file)
    return res

def open_csv(file_csv):
    items = []
    with open(file_csv,  'r', encoding='utf-8') as file:
        data = csv.reader(file, delimiter=';')
        data.__next__()
        for row in data:
            if len(row) == 0: 
                continue
            item = dict()
            item['job'] = row[0]
            item['salary'] = int(row[1])
            item['id'] = int(row[2])
            item['city'] = row[3]
            item['year'] = int(row[4])
            item['age'] = int(row[5])

            items.append(item)
    return items

def open_msgpack(file_msgpack):
    with open(file_msgpack, "rb") as file:
        res = msgpack.unpackb(file.read())
    return res

def insert_many(collection, data):
    collection.insert_many(data)
    
def delete_salary(collection):
    q = {"$or": [{"salary": {"$lt": 25000}},
                 {"salary": {"$gt": 175000}}]}

    collection.delete_many(q)

def added_age(collection):
    collection.update_many({}, {"$inc":{"age": 1}})


def added_salary_job(collection):
    collection.update_many({"job": {"$in": ["Учитель", "Врач"]}},
                                 {"$mul": {"salary": 1.05}})

def added_salary_city(collection):
    collection.update_many({"city": {"$in": ["Эль-Пуэрто-де-Санта-Мария", "Мерида", "Хихон"]}},
                                 {"$mul": {"salary": 1.07}})

def added_salary(collection):
    collection.update_many({"$and": [{"city": {"$in": ["Льейда", "Камбадос", "Подгорица"]}},
                                          {"job": {"$in": ["Баку", "Повар"]}},
                                           {"age": {"$gt": 25, "$lt": 45}}]},
                                 {"$mul": {"salary": 1.1}})

def delete_age(collection):
    q = {"age": {"$gt": 40}}
    collection.delete_many(q)


data=[]
# data.extend(open_pkl(data_file_pkl))
# data.extend(open_csv(data_file_csv))
# data.extend(open_msgpack(data_file_msgpack))
# insert_many(connect(), data)

delete_salary(connect())
added_age(connect())
added_salary(connect())
added_salary_city(connect())
added_salary(connect())
delete_age(connect())