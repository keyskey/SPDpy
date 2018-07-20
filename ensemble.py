import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.size']=20
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

tick = [0.0, "", 0.2, "", 0.4, "", 0.6, "", 0.8, "", 1.0]
sns.heatmap(df_ensembled_pivot, 
            vmin = 0.0, vmax = 1.0, 
            annot = True, 
            cbar = False,
            cmap = "jet",
            square = True,
            xticklabels = tick,
            yticklabels = tick)

plt.gca().invert_yaxis()
plt.tight_layout()
plt.title("Ensemble Average of 100 Realizations")
plt.savefig('ensemble.png')
plt.show()
