import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

num_ens = 2

"""
Create ensemble averaged dataframe(df_ensembled)
"""
df_list = []

for i in range(num_ens):
    df = pd.read_csv(f"phase_diagram{i}.csv") 
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

sns.heatmap(df_variance_pivot,
            vmin = 0, vmax = 0.3,
            annot = False, 
            cbar = True,
            cmap = "jet",
            square = True,
            xticklabels = 2,
            yticklabels = 2)           #cbar_kws={"orientation": "horizontal"}

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('variance.png')
plt.show()
