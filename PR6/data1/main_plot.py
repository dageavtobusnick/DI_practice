import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

first = os.path.join(os.path.dirname(__file__), os.path.normpath('df.csv'))
types = os.path.join(os.path.dirname(__file__), os.path.normpath('dtypes.json'))
res_file_v_name_2 = os.path.join(os.path.dirname(__file__), os.path.normpath('v_name_2.png'))
res_file_v_name = os.path.join(os.path.dirname(__file__), os.path.normpath('v_name.png'))
res_file_h_hits = os.path.join(os.path.dirname(__file__), os.path.normpath('number_h_hits.png'))
res_file_length_minutes_on_h_hits = os.path.join(os.path.dirname(__file__), os.path.normpath('length_minutes_on_h_hits.png'))
res_file_error_on_h_hits_1 = os.path.join(os.path.dirname(__file__), os.path.normpath('error_on_h_hits_1.png'))

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_types():
    with open(types, mode='r') as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] == 'category':
            dtypes[key] = pd.CategoricalDtype()
        else:
            dtypes[key] = np.dtype(dtypes[key])
    return dtypes


need_dtypes = read_types()
dataset = pd.read_csv(first, usecols=lambda x: x in need_dtypes.keys(),
            dtype=need_dtypes)

dataset.info(memory_usage='deep')

plot = sns.histplot(data=dataset, x="v_name", hue="v_name", bins=100)
plot.get_figure().savefig(res_file_v_name_2)

plot = dataset['v_name'].hist()
plot.get_figure().savefig(res_file_v_name)

d2 = dataset.groupby(['h_hits'])['h_hits'].count()
circ = d2.plot(kind='pie', y=d2.keys())
circ.get_figure().savefig(res_file_h_hits)

plt.figure(figsize=(30,5))
plt.plot(dataset.groupby(["v_name"])['h_hits'].sum().values, marker='*', color='green')
plt.savefig(res_file_length_minutes_on_h_hits)

plot = sns.boxplot(data=dataset, x='h_hits', y='h_errors')
plot.get_figure().savefig(res_file_error_on_h_hits_1)
