import json
import os
import pickle
from pymongo import MongoClient

data_file = os.path.join(os.path.dirname(__file__), os.path.normpath('task_1_item.pkl'))
res_file_sort_salary=os.path.join(os.path.dirname(__file__),os.path.normpath("sort_salary.json"))
res_file_filter_age= os.path.join(os.path.dirname(__file__),os.path.normpath("filter_age.json"))
res_file_filter_city=os.path.join(os.path.dirname(__file__),os.path.normpath("filter_city.json"))
res_file_filter_complex= os.path.join(os.path.dirname(__file__),os.path.normpath("filter_complex.json"))

def connect():
    client = MongoClient()
    db = client["database-1"]
    return db.person_data

def open_json(file_json):
    with open(file_json, "rb") as file:
        res = pickle.load(file)
    return res

def insert_many(collection, data):
    collection.insert_many(data)

def sort_salary(collection):

    items = []
    for person in collection.find({}, limit=10).sort({"salary": -1}):
        person["_id"] = str(person["_id"])
        items.append(person)

    with open(res_file_sort_salary, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def filter_age(collection):
    items = []
    for person in collection.find({"age": {"$lt" : 30}}, limit=15).sort({"salary": -1}):
        person["_id"] = str(person["_id"])
        items.append(person)

    with open(res_file_filter_age, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def filter_city(collection):
    items = []
    for person in (collection.find({"city": "Санкт-Петербург", "job":{"$in" : ["Строитель", "Психолог", "Инженер"]}}, limit=10)
            .sort({"age": 1})):
        person["_id"] = str(person["_id"])
        items.append(person)

    with open(res_file_filter_city, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def filter_complex(collection):
    items = []
    for person in (collection.find({
        "age": {"$gt": 22, "$lt": 45},
        "year": {"$in": [2019, 2020, 2021, 2022]},
        "$or": [{"salary": {"$gt": 50000, "$lte": 75000}},
                {"salary": {"$gt": 125000, "$lt": 150000}}]
                                    })):
        person["_id"] = str(person["_id"])
        items.append(person)

    with open(res_file_filter_complex, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))


data = open_json(data_file)
# insert_many(connect(), data)
sort_salary(connect())
filter_age(connect())
filter_city(connect())
filter_complex(connect())
