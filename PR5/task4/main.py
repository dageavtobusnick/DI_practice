import msgpack
import json
import csv
import os
import pickle
from pymongo import MongoClient

data_file_json = os.path.join(os.path.dirname(__file__), os.path.normpath('netflix_rating.json'))
data_file_msgpack = os.path.join(os.path.dirname(__file__), os.path.normpath('netflix_rating.msgpack'))

res_file_sort_imdb_score=os.path.join(os.path.dirname(__file__),os.path.normpath("sort_imdb_score.json"))
res_file_filter_imdb_score=os.path.join(os.path.dirname(__file__),os.path.normpath("filter_imdb_score.json"))
res_file_filter_release_year=os.path.join(os.path.dirname(__file__),os.path.normpath("filter_release_year.json"))
res_file_filter_imdb_votes=os.path.join(os.path.dirname(__file__),os.path.normpath("filter_imdb_votes.json"))
res_file_describe_imdb_score=os.path.join(os.path.dirname(__file__),os.path.normpath("describe_imdb_score.json"))

res_file_count_age_certification=os.path.join(os.path.dirname(__file__),os.path.normpath("count_age_certification.json"))
res_file_rating_age_certification=os.path.join(os.path.dirname(__file__),os.path.normpath("rating_age_certification.json"))
res_file_max_imdb_votes_min_runtime=os.path.join(os.path.dirname(__file__),os.path.normpath("max_imdb_votes_min_runtime.json"))
res_file_describe_release_year=os.path.join(os.path.dirname(__file__),os.path.normpath("describe_release_year.json"))
res_file_sort_release_year=os.path.join(os.path.dirname(__file__),os.path.normpath("sort_release_year.json"))

def connect():
    client = MongoClient()
    db = client["database-2"]
    return db.person_data

def insert_many(collection, data):
    collection.insert_many(data)

def open_json(file_json):
    with open(file_json, "r",encoding='utf-8') as file:
        res = json.load(file)
    return res

def open_msgpack(file_msgpack):
    with open(file_msgpack, "rb") as file:
        res = msgpack.unpackb(file.read())
    return res


def sort_imdb_score(collection):

    items = []
    for game in collection.find({}, limit=20).sort({"imdb_score": -1}):
        game["_id"] = str(game["_id"])
        items.append(game)

    with open(res_file_sort_imdb_score, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def sort_release_year(collection):

    items = []
    for game in collection.find({}, limit=30).sort({"release_year": 1}):
        game["_id"] = str(game["_id"])
        items.append(game)

    with open(res_file_sort_release_year, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def filter_imdb_score(collection):
    items = []
    for game in collection.find({"imdb_score": {"$lt": 5}}, limit=10).sort({"runtime": -1}):
        game["_id"] = str(game["_id"])
        print(game)
        items.append(game)

    with open(res_file_filter_imdb_score, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def filter_release_year(collection):
    items = []
    for game in (collection.find({"age_certification": "R", "release_year":{"$in" : [1979, 1980, 1985]}}, limit=10)
            .sort({"time_on_game": 1})):
        game["_id"] = str(game["_id"])
        items.append(game)

    with open(res_file_filter_release_year, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def filter_imdb_votes(collection):
    items = []
    for game in (collection.find({
                "$or": [{"imdb_votes": {"$gt": 500000, "$lte": 600000}},
                {"imdb_votes": {"$gt": 100000, "$lt": 200000}}]
                                    })):
        game["_id"] = str(game["_id"])
        items.append(game)

    with open(res_file_filter_imdb_votes, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def describe_imdb_score(collection):
    q = [
        {"$group": {"_id": "res", "max": {"$max":"$imdb_score"},
                                  "min": {"$min":"$imdb_score"},
                                  "avg": {"$avg":"$imdb_score"}}}
    ]
    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_describe_imdb_score, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def count_age_certification(collection):
    q = [
        {"$group": {"_id": "$age_certification", "count_name":{"$sum": 1}}},
        {"$sort": {"imdb_votes":-1}}
    ]
    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_count_age_certification, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def rating_age_certification(collection):
    q = [
        {"$group": {"_id": "$age_certification",
                    "max_imdb_votes":{"$max": "$imdb_votes"},
                    "min_imdb_votes": {"$min": "$imdb_votes"},
                    "avg_imdb_votes":{"$avg": "$imdb_votes"}}
         },
        {"$sort": {"index":1}}
    ]
    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_rating_age_certification, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def max_imdb_votes_min_runtime(collection):
    q = [
        {"$group": {"_id": "$age_certification",
                    "min_runtime": {"$min": "$runtime"},
                    "max_imdb_votes": {"$max": "$imdb_votes"}}
        }
        ]
    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_max_imdb_votes_min_runtime, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

def describe_release_year(collection):
    q = [
        {"$match": {"age_certification": "TV-PG"}},
        {"$group": {"_id": "$title",
                    "max_release_year": {"$max": "$min_release_year"},
                    "min_release_year": {"$min": "$min_release_year"},
                    "avg_release_year": {"$avg": "$min_release_year"}}
        },
        {"$sort": {"index": 1}}
        ]
    items = []
    for row in collection.aggregate(q):
        items.append(row)

    with open(res_file_describe_release_year, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))


def delete_imdb_score(collection):
    q = {"imdb_score": {"$lt": 3}}

    collection.delete_many(q)

def added_runtime(collection):
    collection.update_many({}, {"$inc":{"runtime": 5}})

def delete_type(collection):
    q = {"type": "SHOW"}
    collection.delete_many(q)

def decrease_imdb_score(collection):
    collection.update_many({"age_certification": {"$in": ["PG-13", "TV-PG"]}},
                                 {"$mul": {"imdb_score": 0.85}})

def added_imdb_score(collection):
    collection.update_many({"$and": [{"imdb_votes": {"$gt": 0, "$lte": 50000}},
                                          {"age_certification": {"$in": ["TV-PG", "PG-13"]}}]},
                                 {"$mul": {"imdb_score": 1.1}})

data=[]

# data.extend(open_json(data_file_json))
# data.extend(open_msgpack(data_file_msgpack))

# insert_many(connect(), data)

sort_imdb_score(connect())
sort_release_year(connect())
filter_imdb_score(connect())
filter_release_year(connect())
filter_imdb_votes(connect())
describe_imdb_score(connect())
count_age_certification(connect())
rating_age_certification(connect())
max_imdb_votes_min_runtime(connect())
describe_release_year(connect())

delete_imdb_score(connect())
added_runtime(connect())
delete_type(connect())
decrease_imdb_score(connect())
added_imdb_score(connect())