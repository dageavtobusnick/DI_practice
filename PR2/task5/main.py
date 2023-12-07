import json
from statistics import mean
from scipy import stats
import msgpack
import pandas as pd
import os

allowed_name_list = ['points',
                     'taster_name',
                     'price',
                     'designation',
                     'variety',
                     'region_1',
                     'region_2',
                     'country',
                     ]

resulting_dict = {}

dataset = []

text_var = 'winemag-data-130k-v2.json'
file_products = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result_json = os.path.join(os.path.dirname(__file__), os.path.normpath('result.json'))
result_msgpack = os.path.join(os.path.dirname(__file__), os.path.normpath('result.msgpack'))
result_csv = os.path.join(os.path.dirname(__file__), os.path.normpath('result.csv'))
result_pkl = os.path.join(os.path.dirname(__file__), os.path.normpath('result.pkl'))

with open(file_products, 'r', encoding='utf-8') as inp:
    dataset = json.load(inp)


for item in dataset:
    for key,value in item.items():
        if(key in allowed_name_list):
            if value is None:
                continue
            if key not in resulting_dict.keys():
                if(isinstance(value, int)):
                    resulting_dict[key]=[]
                else:
                    resulting_dict[key]={}
            if(isinstance(value, int)):
                resulting_dict[key].append(value)
            else:
                if(value in resulting_dict[key].keys()):
                    resulting_dict[key][value]+=1
                else:
                    resulting_dict[key][value]=1
                    


def resolve_strategy(data, metric_name):
    if isinstance(data, dict):
        return process_str(data, metric_name)
    if isinstance(data, list):
        return process_numeric(data, metric_name)

    raise


def process_str(dict: {}, name: str):
    return {
        name: json.dumps(dict)
    }


def process_numeric(data_list: [], name: str):
    filtered_list = list(filter(lambda x: x is not None, data_list))
    mapped_list = list(map(lambda x: float(x), filtered_list))

    return {
        name: {
            'avg': mean(mapped_list),
            'min': min(mapped_list),
            'max': max(mapped_list),
            'sum': sum(mapped_list),
            'std_err': stats.sem(mapped_list)
        }
    }



result = list(map(lambda x: resolve_strategy(resulting_dict[x], x), list(resulting_dict.keys())))

with open(result_json, 'w', encoding='utf-8') as out:
    out.write(json.dumps(result))

with open(result_msgpack , 'wb') as out:
    out.write(msgpack.packb(dataset))

df = pd.DataFrame([x for x in dataset])

with open(result_csv, 'w', encoding='utf-8') as out:
    out.write(df.to_csv(index=False))

df.to_pickle(result_pkl)

file_stats_json = os.stat(result_json)
file_stats_csv = os.stat(result_json)
file_stats_msgpack = os.stat(result_msgpack)
file_stats_pickle = os.stat(result_pkl)
print("Размер json файла в байтах: ", file_stats_json.st_size)
print("Размер csv файла в байтах: ", file_stats_csv.st_size)
print("Размер msgpack файла в байтах: ", file_stats_msgpack.st_size)
print("Размер pkl файла в байтах: ", file_stats_pickle.st_size)