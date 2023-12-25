import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

first = os.path.join(os.path.dirname(__file__), os.path.normpath('df_6.csv'))
types = os.path.join(os.path.dirname(__file__), os.path.normpath('dtypes_6.json'))
res_file_ProductId = os.path.join(os.path.dirname(__file__), os.path.normpath('ProductId.png'))
res_file_UserId_v1 = os.path.join(os.path.dirname(__file__), os.path.normpath('UserId_v1.png'))
res_file_UserId = os.path.join(os.path.dirname(__file__), os.path.normpath('UserId.png'))
res_file_UserId_Score = os.path.join(os.path.dirname(__file__), os.path.normpath('UserId_Score.png'))
res_file_Score_ProductId = os.path.join(os.path.dirname(__file__), os.path.normpath('Score_ProductId.png'))


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


dataset.info(memory_usage='deep')


plot = sns.histplot(data=dataset, x="Qualifications", hue="Qualifications", bins=100)
plot.get_figure().savefig(res_file_ProductId)

plot = dataset['Role'].hist()
plot.get_figure().savefig(res_file_UserId_v1)

d2 = dataset.groupby(['Role'])['Role'].count()
circ = d2.plot(kind='pie', y=d2.keys(), autopct='%1.0f%%', title='')
circ.get_figure().savefig(res_file_UserId)

plt.figure(figsize=(15,10))
plt.plot(dataset.groupby(["Qualifications"])['longitude'].sum().values, marker='*', color='green')
plt.savefig(res_file_UserId_Score)

plot = sns.boxplot(data=dataset, x='Company Size', y='Role')
plot.get_figure().savefig(res_file_Score_ProductId)
