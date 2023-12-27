import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

first = os.path.join(os.path.dirname(__file__), os.path.normpath('df_5.csv'))
types = os.path.join(os.path.dirname(__file__), os.path.normpath('dtypes_5.json'))
res_file_diameter = os.path.join(os.path.dirname(__file__), os.path.normpath('diameter.png'))
res_file_class_v1 = os.path.join(os.path.dirname(__file__), os.path.normpath('class_v1.png'))
res_file_MBA = os.path.join(os.path.dirname(__file__), os.path.normpath('MBA.png'))
res_file_experience_albedo = os.path.join(os.path.dirname(__file__), os.path.normpath('experience_albedo.png'))
res_file_experience_sigma_w = os.path.join(os.path.dirname(__file__), os.path.normpath('experience_sigma_w.png'))


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
grouped_df = dataset.groupby('diameter_group')['diameter_sigma'].mean().reset_index()
plt.plot(grouped_df['diameter_group'], grouped_df['diameter_sigma'])
plt.savefig(res_file_diameter)
plt.close()

plot = sns.histplot(data=dataset, x="class", hue="class", bins=100)
plot.get_figure().savefig(res_file_class_v1)
plt.close()

data = dataset[dataset['class'] != 'MBA']
d2 = data.groupby(['class'])['class'].count()
d2 = d2[d2 > len(data) * 0.05]
circ = d2.plot(kind='pie', y=d2.keys(), autopct='%1.0f%%', title='')
plt.tight_layout()
circ.get_figure().savefig(res_file_MBA)
plt.close()

plot = sns.boxplot(data=dataset, x='albedo', y='class')
plot.get_figure().savefig(res_file_experience_albedo)
plt.close()


plt.figure(figsize=(15,10))
plt.plot(dataset.sample(1000).groupby(["albedo"])['sigma_w'].sum().values, marker='*', color='green')
plt.savefig(res_file_experience_sigma_w)
plt.close()

