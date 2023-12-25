import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

first = os.path.join(os.path.dirname(__file__), os.path.normpath('df_5.csv'))
types = os.path.join(os.path.dirname(__file__), os.path.normpath('dtypes_5.json'))
res_file_diameter = os.path.join(os.path.dirname(__file__), os.path.normpath('diameter.png'))
res_file_diameter_v1 = os.path.join(os.path.dirname(__file__), os.path.normpath('diameter_v1.png'))
res_file_MBA = os.path.join(os.path.dirname(__file__), os.path.normpath('MBA.png'))
res_file_experience_moid = os.path.join(os.path.dirname(__file__), os.path.normpath('experience_moid .png'))
res_file_experience_sigma_per = os.path.join(os.path.dirname(__file__), os.path.normpath('experience_sigma_per.png'))


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


dataset['diameter_group'] = (dataset['diameter'] // 10) * 10
grouped_df = dataset.groupby('diameter_group')['diameter'].mean().reset_index()
plt.plot(grouped_df['diameter_group'], grouped_df['diameter'])
plt.savefig(res_file_diameter)

plot = sns.histplot(data=grouped_df, x="diameter", hue="diameter", bins=100)
plot.get_figure().savefig(res_file_diameter_v1)

data = dataset[dataset['class'] != 'MBA']
d2 = data.groupby(['class'])['class'].count()
d2 = d2[d2 > len(data) * 0.05]
circ = d2.plot(kind='pie', y=d2.keys(), autopct='%1.0f%%', title='')
plt.tight_layout()
circ.get_figure().savefig(res_file_MBA)

plot = sns.boxplot(data=dataset, x='moid', y='class')
plot.get_figure().savefig(res_file_experience_moid)


plt.figure(figsize=(15,10))
plt.plot(dataset.groupby(["sigma_per"])['sigma_w'].sum().values, marker='*', color='green')
plt.savefig(res_file_experience_sigma_per)

