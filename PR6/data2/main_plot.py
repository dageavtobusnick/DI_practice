import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

first = os.path.join(os.path.dirname(__file__), os.path.normpath('df_2.csv'))
types = os.path.join(os.path.dirname(__file__), os.path.normpath('dtypes_2.json'))
res_file_brandName = os.path.join(os.path.dirname(__file__), os.path.normpath('brandName.png'))
res_file_modelName = os.path.join(os.path.dirname(__file__), os.path.normpath('modelName.png'))
res_file_modelName_v1 = os.path.join(os.path.dirname(__file__), os.path.normpath('modelName_v1.png'))
res_file_msrp_brandName = os.path.join(os.path.dirname(__file__), os.path.normpath('msrp_brandName.png'))
res_file_vf_Windows_vf_Wheels = os.path.join(os.path.dirname(__file__), os.path.normpath('vf_Windows_vf_Wheels.png'))

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

plot = sns.histplot(data=dataset, x="brandName", hue="brandName", bins=100)
plt.xticks(rotation=45)
plot.get_figure().savefig(res_file_brandName)
plot = dataset['modelName'].hist()
plot.get_figure().savefig(res_file_modelName_v1)

d2 = dataset.groupby(['modelName'])['modelName'].count()
circ = d2.plot(kind='pie', y=d2.keys(), autopct='%1.0f%%', title='')
circ.get_figure().savefig(res_file_modelName)

plt.figure(figsize=(15,10))
plt.plot(dataset.groupby(["brandName"])['msrp'].sum().values, marker='*', color='green')
plt.savefig(res_file_msrp_brandName)

plot = sns.boxplot(data=dataset, x='vf_Windows', y='vf_Wheels')
plot.get_figure().savefig(res_file_vf_Windows_vf_Wheels)
