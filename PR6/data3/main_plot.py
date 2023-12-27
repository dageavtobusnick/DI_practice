import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

first = os.path.join(os.path.dirname(__file__), os.path.normpath('df_3.csv'))
types = os.path.join(os.path.dirname(__file__), os.path.normpath('dtypes_3.json'))
res_file_AIRLINE = os.path.join(os.path.dirname(__file__), os.path.normpath('AIRLINE.png'))
res_file_DAY_OF_WEEK = os.path.join(os.path.dirname(__file__), os.path.normpath('DAY_OF_WEEK.png'))
res_file_ORIGIN_AIRPORT = os.path.join(os.path.dirname(__file__), os.path.normpath('ORIGIN_AIRPORT.png'))
res_file_ORIGIN_AIRPORT_SCHEDULED_TIME = os.path.join(os.path.dirname(__file__), os.path.normpath('ORIGIN_AIRPORT_SCHEDULED_TIME.png'))
res_file_vf_AIR_TIME_in_DAY_OF_WEEK = os.path.join(os.path.dirname(__file__), os.path.normpath('AIR_TIME_in_DAY_OF_WEEK.png'))

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_types():
    with open(types, mode='r') as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] == 'category':
            dtypes[key] = pd.CategoricalDtype()
        elif dtypes[key] == 'string':
            dtypes[key] = pd.StringDtype()
        else:
            dtypes[key] = np.dtype(dtypes[key])
    return dtypes


need_dtypes = read_types()

dataset = pd.read_csv(first, usecols=lambda x: x in need_dtypes.keys(),
            dtype=need_dtypes)

dataset.info(memory_usage='deep')

plot = sns.histplot(data=dataset, x="AIRLINE", hue="AIRLINE", bins=100)
plot.get_figure().savefig(res_file_AIRLINE)
plt.xticks(rotation=45)
plt.close()

plot = dataset['DAY_OF_WEEK'].hist()
plot.get_figure().savefig(res_file_ORIGIN_AIRPORT)
plt.close()

d2 = dataset.groupby(['DAY_OF_WEEK'])['DAY_OF_WEEK'].count()
circ = d2.plot(kind='pie', y=d2.keys(), autopct='%1.0f%%', title='')
circ.get_figure().savefig(res_file_DAY_OF_WEEK)
plt.close()

plt.figure(figsize=(15,10))
plt.plot(dataset.groupby(["ORIGIN_AIRPORT"])['SCHEDULED_TIME'].sum().values, marker='*', color='green')
plt.savefig(res_file_ORIGIN_AIRPORT_SCHEDULED_TIME)
plt.close()

plot = sns.boxplot(data=dataset.sample(1000), x='DAY_OF_WEEK', y='AIR_TIME')
plot.get_figure().savefig(res_file_vf_AIR_TIME_in_DAY_OF_WEEK)
plt.close()

