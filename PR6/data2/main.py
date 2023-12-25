import functions
import os
import pandas as pd
import json

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('[2]automotive.csv.zip'))
my_file_unp = os.path.join(os.path.dirname(__file__), os.path.normpath('CIS_Automotive_Kaggle_Sample.csv'))
res_file_df=os.path.join(os.path.dirname(__file__), os.path.normpath('df_2.csv'))
res_file_dtypes=os.path.join(os.path.dirname(__file__), os.path.normpath("dtypes_2.json"))
pd.set_option("display.max_rows", 20, "display.max_columns", 60)


functions.get_memory_stat_no_opt(my_file)

column_dtype = {
    'firstSeen': pd.StringDtype(),
    'brandName': pd.CategoricalDtype(),
    'modelName': pd.CategoricalDtype(),
    'msrp': pd.StringDtype(),
    'isNew': pd.CategoricalDtype(),
    'color': pd.CategoricalDtype(),
    'vf_Wheels': pd.StringDtype(),
    'vf_Seats': pd.StringDtype(),
    'vf_Windows': pd.StringDtype(),
    'vf_WheelBaseShort': pd.StringDtype()
}

has_header = True
total_size = 0
for part in pd.read_csv(my_file, usecols = lambda x: x in column_dtype.keys(), 
                               chunksize=500_000, compression='zip'):
    total_size += part.memory_usage(deep=True).sum()
    print(part.shape)
    part.dropna().to_csv(res_file_df, mode='a', header=has_header)
    print(part.shape)
    has_header = False
print(total_size)
 

def read_file(file_name):
    return pd.read_csv(file_name)

dataset = read_file(res_file_df)
converted_obj = functions.opt_obj(dataset)
converted_int = functions.opt_int(dataset)
converted_float =  functions.opt_float(dataset)

optimized_dataset = dataset.copy()

optimized_dataset[converted_obj.columns] = converted_obj
optimized_dataset[converted_int.columns] = converted_int
optimized_dataset[converted_float.columns] = converted_float

print(functions.mem_usage(dataset))
print(functions.mem_usage(optimized_dataset))
functions.get_memory_with_optim(optimized_dataset,my_file_unp)

need_column = {}
opt_dtypes = optimized_dataset.dtypes
print(opt_dtypes)
for key in dataset.columns:
    need_column[key] = opt_dtypes[key]
    print(f'{key}:{opt_dtypes[key]}')

with open(res_file_dtypes, mode='w') as file:
    dtypes_json = need_column.copy()
    for key in dtypes_json.keys():
        dtypes_json[key] = str(dtypes_json[key])
    print(dtypes_json)
    json.dump(dtypes_json, file)

