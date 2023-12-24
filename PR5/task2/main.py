import json
import csv
import os
import pickle
from pymongo import MongoClient

data_file_pkl = os.path.join(os.path.dirname(__file__), os.path.normpath('task_1_item.pkl'))
data_file_csv = os.path.join(os.path.dirname(__file__), os.path.normpath('task_2_item.csv'))
res_file_describe_salary=os.path.join(os.path.dirname(__file__),os.path.normpath("describe_salary.json"))
res_file_count_job= os.path.join(os.path.dirname(__file__),os.path.normpath("count_job.json"))
res_file_salary_city=os.path.join(os.path.dirname(__file__),os.path.normpath("salary_city.json"))
res_file_salary_job=os.path.join(os.path.dirname(__file__),os.path.normpath("salary_job.json"))
res_file_age_sity= os.path.join(os.path.dirname(__file__),os.path.normpath("age_sity.json"))
res_file_age_job= os.path.join(os.path.dirname(__file__),os.path.normpath("age_job.json"))
res_file_max_salary_min_age= os.path.join(os.path.dirname(__file__),os.path.normpath("max_salary_min_age.json"))
res_file_min_salary_max_age= os.path.join(os.path.dirname(__file__),os.path.normpath("min_salary_max_age.json"))
res_file_describe_age_sity= os.path.join(os.path.dirname(__file__),os.path.normpath("describe_age_sity.json"))
res_file_describe_salary_sity= os.path.join(os.path.dirname(__file__),os.path.normpath("describe_salary_sity.json"))
res_file_describe_salary_job= os.path.join(os.path.dirname(__file__),os.path.normpath("describe_salary_job.json"))
res_file_describe_salary_age= os.path.join(os.path.dirname(__file__),os.path.normpath("describe_salary_age.json"))
res_file_my_request= os.path.join(os.path.dirname(__file__),os.path.normpath("my_request.json"))

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


def insert_many(collection, data):
    collection.insert_many(data)
    
def describe_salary(collection):
    q = [
        {"$group": {"_id": "res", "max": {"$max":"$salary"},
                                  "min": {"$min":"$salary"},
                                  "avg": {"$avg":"$salary"}}}
    ]
    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_describe_salary, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))


def count_job(collection):
    q = [
        {"$group": {"_id": "$job", "count_job":{"$sum": 1}}},
        {"$sort": {"count_job":-1}}
    ]
    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_count_job, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def salary_city(collection):
    q = [
        {"$group": {"_id": "$city",
                    "max_salary":{"$max": "$salary"},
                    "min_salary": {"$min": "$salary"},
                    "avg_salary":{"$avg": "$salary"}}
         },
        {"$sort": {"_id":1}}
    ]
    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_salary_city, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def salary_job(collection):
    q = [
        {"$group": {"_id": "$job",
                    "max_salary":{"$max": "$salary"},
                    "min_salary": {"$min": "$salary"},
                    "avg_salary":{"$avg": "$salary"}}
         },
        {"$sort": {"_id":1}}
    ]
    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_salary_job, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def age_sity(collection):
    q = [
        {"$group": {"_id": "$city",
                    "max_age":{"$max": "$age"},
                    "min_age": {"$min": "$age"},
                    "avg_age":{"$avg": "$age"}}
         },
        {"$sort": {"_id":1}}
    ]
    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_age_sity, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def age_job(collection):
    q = [
        {"$group": {"_id": "$job",
                    "max_age":{"$max": "$age"},
                    "min_age": {"$min": "$age"},
                    "avg_age":{"$avg": "$age"}}
         },
        {"$sort": {"_id":1}}
    ]
    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_age_job, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def max_salary_min_age(collection):
    q = [
            {
                '$sort': {
                    'age': -1,
                    'salary': 1
                }
            },
            {
                  '$limit': 1
            }
        ]
    items = []
    for row in collection.aggregate(q):
        row['_id']=str(row['_id'])
        items.append(row)

    with open(res_file_max_salary_min_age, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def min_salary_max_age(collection):
    q = [
            {
                '$sort': {
                    'age': 1,
                    'salary': -1
                }
            },
            {
                  '$limit': 1
            }
        ]
    items = []
    for row in collection.aggregate(q):
        row['_id']=str(row['_id'])
        items.append(row)
    with open(res_file_min_salary_max_age, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def describe_age_sity(collection):
    q = [
        {"$match": {"salary": {"$gt": 50000}}},
        {"$group": {"_id": "$city",
                    "max_age": {"$max": "$age"},
                    "min_age": {"$min": "$age"},
                    "avg_age": {"$avg": "$age"}}
        },
        {"$sort": {"_id": 1}}
        ]

    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_describe_age_sity, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def describe_salary_sity(collection):
    q = [
        {"$match": {"$or": [{"age": {"$gt": 18, "$lte": 25}},
                {"age": {"$gt": 50, "$lt": 65}}]}},
        {"$group": {"_id": "$city",
                    "max_salary": {"$max": "$salary"},
                    "min_salary": {"$min": "$salary"},
                    "avg_salary": {"$avg": "$salary"}}
        },
        {"$sort": {"_id": 1}}
        ]

    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_describe_salary_sity, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def describe_salary_job(collection):
    q = [
        {"$match": {"$or": [{"age": {"$gt": 18, "$lte": 25}},
                {"age": {"$gt": 50, "$lt": 65}}]}},
        {"$group": {"_id": "$job",
                    "max_salary": {"$max": "$salary"},
                    "min_salary": {"$min": "$salary"},
                    "avg_salary": {"$avg": "$salary"}}
        },
        {"$sort": {"_id": 1}}
        ]

    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_describe_salary_job, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def describe_salary_age(collection):
    q = [
        {"$match": {"$or": [{"age": {"$gt": 18, "$lte": 25}},
                {"age": {"$gt": 50, "$lt": 65}}]}},
        {"$group": {"_id": "$age",
                    "max_salary": {"$max": "$salary"},
                    "min_salary": {"$min": "$salary"},
                    "avg_salary": {"$avg": "$salary"}}
        },
        {"$sort": {"_id": 1}}
        ]

    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_describe_salary_age, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def my_request(collection):
    q = [
        {"$match": {"job": "IT-специалист"}},
        {"$group": {"_id": "$city",
                    "max_age": {"$max": "$age"},
                    "min_age": {"$min": "$age"},
                    "avg_age": {"$avg": "$age"}}
        },
        {"$sort": {"_id": 1}}
        ]

    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_my_request, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))
    
data=[]
# data.extend(open_pkl(data_file_pkl))
# data.extend(open_csv(data_file_csv))
# insert_many(connect(), data)
describe_salary(connect())
count_job(connect())
salary_city(connect())
salary_job(connect())
age_sity(connect())
age_job(connect())
max_salary_min_age(connect())
min_salary_max_age(connect())
describe_age_sity(connect())
describe_salary_sity(connect())
describe_salary_job(connect())
describe_salary_age(connect())
my_request(connect())