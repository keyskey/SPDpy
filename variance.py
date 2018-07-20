import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

num_ens = 100

df_list = []

for i in range(1, num_ens + 1):
    df = pd.read_csv('output{}.csv'.format(i)) 
    df_list.append(df)

df_ensembled = df_list[0]

for df in df_list[1:]:
    df_ensembled['Fraction of Cooperation'] += df['Fraction of Cooperation']

df_ensembled['Fraction of Cooperation'] =  df_ensembled['Fraction of Cooperation']/num_ens   
df_ensembled_pivot = df_ensembled.pivot('Dg','Dr', 'Fraction of Cooperation')
mu = df_ensembled['Fraction of Cooperation']
#print(mu)

plt.rcParams['font.size'] = 20
#plt.rcParams['figure.figsize'] = 20,20
df_list2 = deepcopy(df_list)

for df in df_list2:
    df['Fraction of Cooperation'] = (df['Fraction of Cooperation'] - mu)**2

df_variance = df_list2[0]

for df in df_list2[1:]:
    df_variance['Fraction of Cooperation'] += df['Fraction of Cooperation']

df_variance['Fraction of Cooperation'] = df_variance['Fraction of Cooperation']/(num_ens-1)
df_variance_pivot = df_variance.pivot('Dg', 'Dr', 'Fraction of Cooperation')

tick = [0.0, "", 0.2, "", 0.4, "", 0.6, "", 0.8, "", 1.0]

sns.heatmap(df_variance_pivot,
            vmin = 0, vmax = 0.3,
            annot = False, 
            cbar = True,
            cmap = "jet",
            square = True,
            xticklabels = tick,
            yticklabels = tick)           #cbar_kws={"orientation": "horizontal"}
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('variance.png')
plt.show()

