import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

plt.rcParams['font.size'] = 20
plt.rcParams['figure.figsize'] = 20,20

num_ens = 100

"""
Create ensemble averaged dataframe(df_ensembled)
"""
df_list = []

for i in range(1, num_ens + 1):
    df = pd.read_csv('output{}.csv'.format(i)) 
    df_list.append(df)

df_ensembled = df_list[0]

for df in df_list[1:]:
    df_ensembled['Fc'] += df['Fc']

df_ensembled['Fc'] =  df_ensembled['Fc']/num_ens   
mu = df_ensembled['Fc']


"""
Calculate the variance over 100 episodes
"""
df_list2 = deepcopy(df_list)

for df in df_list2:
    df['Fc'] = (df['Fc'] - mu)**2

df_variance = df_list2[0]

for df in df_list2[1:]:
    df_variance['Fc'] += df['Fc']

df_variance['Fc'] = df_variance['Fc']/(num_ens-1)
df_variance_pivot = df_variance.pivot('Dg', 'Dr', 'Fc')

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
