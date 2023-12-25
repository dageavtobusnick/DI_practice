import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

first = os.path.join(os.path.dirname(__file__), os.path.normpath('df_4.csv'))
types = os.path.join(os.path.dirname(__file__), os.path.normpath('dtypes_4.json'))
res_file_schedule_name = os.path.join(os.path.dirname(__file__), os.path.normpath('schedule_name.png'))
res_file_experience_name_v1 = os.path.join(os.path.dirname(__file__), os.path.normpath('experience_name_v1.png'))
res_file_experience_name = os.path.join(os.path.dirname(__file__), os.path.normpath('experience_name.png'))
res_file_experience_name_salary_from = os.path.join(os.path.dirname(__file__), os.path.normpath('experience_name_salary_from.png'))
res_file_salary_from_experience_name = os.path.join(os.path.dirname(__file__), os.path.normpath('salary_from_experience_name.png'))


pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_types():
    with open(types , mode='r') as file:
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


plot = sns.histplot(data=dataset, x="schedule_name", hue="schedule_name", bins=100)
plot.get_figure().savefig(res_file_schedule_name)

plot = dataset['experience_name'].hist()
plot.get_figure().savefig(res_file_experience_name_v1)

d2 = dataset.groupby(['experience_name'])['experience_name'].count()
circ = d2.plot(kind='pie', y=d2.keys(), autopct='%1.0f%%', title='')
circ.get_figure().savefig(res_file_experience_name)

plt.figure(figsize=(15,10))
plt.plot(dataset.groupby(["experience_name"])['salary_from'].sum().values, marker='*', color='green')
plt.savefig(res_file_experience_name_salary_from)

plot = sns.boxplot(data=dataset, x='salary_from', y='experience_name')
plot.get_figure().savefig(res_file_salary_from_experience_name)
