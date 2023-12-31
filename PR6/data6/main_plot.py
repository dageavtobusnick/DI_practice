import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

first = os.path.join(os.path.dirname(__file__), os.path.normpath('df_6.csv'))
types = os.path.join(os.path.dirname(__file__), os.path.normpath('dtypes_6.json'))
res_file_Qualifications = os.path.join(os.path.dirname(__file__), os.path.normpath('Qualifications.png'))
res_file_Qualifications_v1= os.path.join(os.path.dirname(__file__), os.path.normpath('Qualifications_v1.png'))
res_file_Qualifications_longitude= os.path.join(os.path.dirname(__file__), os.path.normpath('Qualifications_longitude.png'))
res_file_Preference = os.path.join(os.path.dirname(__file__), os.path.normpath('Preference.png'))
res_file_Company_Size_Qualifications = os.path.join(os.path.dirname(__file__), os.path.normpath('Company_Size_Qualifications.png'))


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


plot = sns.histplot(data=dataset.sample(1000), x="Qualifications", hue="Qualifications", bins=100)
plot.get_figure().savefig(res_file_Qualifications)
plt.close()

plot = dataset.sample(1000)['Qualifications'].hist()
plot.get_figure().savefig(res_file_Qualifications_v1)
plt.close()

d2 = dataset.sample(1000).groupby(['Preference'])['Preference'].count()
circ = d2.plot(kind='pie', y=d2.keys(), autopct='%1.0f%%', title='')
circ.get_figure().savefig(res_file_Preference)
plt.close()

plt.figure(figsize=(15,10))
plt.plot(dataset.sample(1000).groupby(["Qualifications"])['longitude'].sum().values, marker='*', color='green')
plt.savefig(res_file_Qualifications_longitude)
plt.close()

plot = sns.boxplot(data=dataset.sample(1000), x='Company Size', y='Qualifications')
plot.get_figure().savefig(res_file_Company_Size_Qualifications)
plt.close()
