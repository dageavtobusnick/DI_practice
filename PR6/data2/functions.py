import pandas as pd
import os
import json

res_file_mem_no_opt = os.path.join(os.path.dirname(__file__), os.path.normpath('colums_memory_no_optim.json'))
res_file_mem_opt = os.path.join(os.path.dirname(__file__), os.path.normpath('colums_memory_with_optim.json'))

def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2
    return "{:03.2f} MB".format(usage_mb)

def get_memory_stat_by_column(df, temp,my_file):
    file_size = os.path.getsize(my_file)
    print(f'file size             = {file_size // 1024:10} КБ')
    memory_update_stat = df.memory_usage(deep=True)
    total_memory_usage = memory_update_stat.sum()
    print(f'file in memory size   = {total_memory_usage // 1024:10} КБ')

    column_stat = []
    for key in df.dtypes.keys():
        column_stat.append({'column_name': key,
                            'memory_abs': int(memory_update_stat[key] // 1024),
                            "memory_per": float(round(memory_update_stat[key] / total_memory_usage * 100, 4)),
                            'dtype': str(df.dtypes[key])})
    column_stat.sort(key=lambda x: x['memory_abs'], reverse=True)
    
    if temp == 0:
        name = res_file_mem_no_opt
    else:
        name = res_file_mem_opt
    with open(name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(column_stat, ensure_ascii=False))
        
def get_memory_stat_no_opt(file_chunk_name):
    file_size = os.path.getsize(file_chunk_name)
    print(f'file size             = {file_size // 1024:10} КБ')

    total_size = 0
    start_data = next(pd.read_csv(file_chunk_name, chunksize=100_000))
    columns_stats = {
        column: {
            'memory_abs': 0,
            'memory_per': 0,
            'dtype': str(start_data.dtypes[column])
        }
        for column in start_data}
    for chunk in pd.read_csv(file_chunk_name, chunksize=100_000):
        chunk_memory = chunk.memory_usage(deep=True)
        total_size += float(chunk_memory.sum())
        for column in chunk:
            columns_stats[column]['memory_abs'] += float(chunk_memory[column])

    for col in columns_stats.keys():
        columns_stats[col]['memory_per'] = round(columns_stats[col]['memory_abs'] / total_size * 100, 4)
        columns_stats[col]['memory_abs'] = columns_stats[col]['memory_abs'] // 1024 
    with open(res_file_mem_no_opt, 'w', encoding='utf-8') as f:
        f.write(json.dumps(columns_stats, ensure_ascii=False))


def get_memory_with_optim(df,my_file):
    file_size = os.path.getsize(my_file)
    print(f'file size             = {file_size // 1024:10} КБ')
    memory_update_stat = df.memory_usage(deep=True)
    total_memory_usage = memory_update_stat.sum()
    print(f'file in memory size   = {total_memory_usage // 1024:10} КБ')

    column_stat = []
    for key in df.dtypes.keys():
        column_stat.append({'column_name': key,
                            'memory_abs': int(memory_update_stat[key] // 1024),
                            "memory_per": float(round(memory_update_stat[key] / total_memory_usage * 100, 4)),
                            'dtype': str(df.dtypes[key])})
    column_stat.sort(key=lambda x: x['memory_abs'], reverse=True)
    with open(res_file_mem_opt, 'w', encoding='utf-8') as f:
        f.write(json.dumps(column_stat, ensure_ascii=False))

def opt_obj(df):
    converted_obj = pd.DataFrame()
    dataset_obj = df.select_dtypes(include=['object']).copy()

    for col in dataset_obj.columns:
        num_unique_values = len(dataset_obj[col].unique())
        num_total_values = len(dataset_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:, col] = dataset_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = dataset_obj[col]

    print(mem_usage(dataset_obj))
    print(mem_usage(converted_obj))
    return converted_obj


def opt_int(df):
    data_int = df.select_dtypes(include=['int'])

    converted_int = data_int.apply(pd.to_numeric, downcast='unsigned')
    print(mem_usage(data_int))
    print(mem_usage(converted_int))

    compare_ints = pd.concat([data_int.dtypes, converted_int.dtypes], axis=1)
    compare_ints.columns = ['before', 'after']
    compare_ints.apply(pd.Series.value_counts)
    print(compare_ints)

    return converted_int

    
def opt_float(df):
    data_float = df.select_dtypes(include=['float'])

    converted_float = data_float.apply(pd.to_numeric, downcast='float')
    print(mem_usage(data_float))
    print(mem_usage(converted_float))

    compare_floats = pd.concat([data_float.dtypes, converted_float.dtypes], axis=1)
    compare_floats.columns = ['before', 'after']
    compare_floats.apply(pd.Series.value_counts)
    print(compare_floats)

    return converted_float