import functions
import os
import pandas as pd
import json

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('[1]game_logs.csv'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))
res_file_mem_no_opot = os.path.join(os.path.dirname(__file__), os.path.normpath('colums_memory_no_optim.json'))
res_file_mem_opot = os.path.join(os.path.dirname(__file__), os.path.normpath('colums_memory_with_optim.json'))
res_file_df=os.path.join(os.path.dirname(__file__), os.path.normpath("df.csv"))
res_file_dtypes=os.path.join(os.path.dirname(__file__), os.path.normpath("dtypes.json"))
pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_file():
    return pd.read_csv(my_file)

data = read_file()

converted_obj = functions.opt_obj(data)
converted_int = functions.opt_int(data)
converted_float =  functions.opt_float(data)

optimized_dataset = data.copy()

optimized_dataset[converted_obj.columns] = converted_obj
optimized_dataset[converted_int.columns] = converted_int
optimized_dataset[converted_float.columns] = converted_float

print(functions.mem_usage(data))
print(functions.mem_usage(optimized_dataset))
functions.get_memory_stat_by_column(optimized_dataset, 1,my_file)

need_column = {}
column_names = ['date', 'number_of_game', 'day_of_week', 'park_id',
                'v_manager_name', 'length_minutes', 'v_hits',
                'h_hits', 'h_walks', 'h_errors'] 
opt_dtypes = optimized_dataset.dtypes
for key in column_names:
    need_column[key] = opt_dtypes[key]
    print(f'{key}:{opt_dtypes[key]}')

with open(res_file_dtypes, mode='w') as file:
    dtypes_json = need_column.copy()
    for key in dtypes_json.keys():
        dtypes_json[key] = str(dtypes_json[key])
    
    json.dump(dtypes_json, file)
read_and_optimized = pd.read_csv(my_file,
                                 usecols = lambda x: x in column_names,
                                 dtype=need_column)

print(read_and_optimized.shape)
print(read_and_optimized)
print(functions.mem_usage(read_and_optimized))

has_header = True    
for chunk in pd.read_csv(my_file,
                        usecols = lambda x: x in column_names,
                        dtype=need_column,
                        # parse_dates=['date'],
                        # infer_datetime_format=True,
                        chunksize=100_000):
    print(functions.mem_usage(chunk))
    chunk.to_csv(res_file_df, mode='a', header=has_header)
    has_header = False