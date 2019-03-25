import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

num_ens = 2
df_list = []

for i in range(num_ens):
    df = pd.read_csv(f"phase_diagram{i}.csv") 
    df_list.append(df)

df_ensembled = df_list[0]

for df in df_list[1:]:
    df_ensembled['Fc'] += df['Fc']

df_ensembled['Fc'] =  df_ensembled['Fc']/num_ens   
df_ensembled_pivot = df_ensembled.pivot('Dg','Dr', 'Fc')

sns.heatmap(df_ensembled_pivot, 
            vmin = 0.0, 
            vmax = 1.0, 
            annot = False, 
            cbar = False,
            cmap = "jet",
            square = True,
            xticklabels = 2,
            yticklabels = 2)

plt.gca().invert_yaxis()
plt.title("Ensemble Average of 100 Realizations")
plt.tight_layout()
plt.savefig('ensemble.png')
plt.show()
