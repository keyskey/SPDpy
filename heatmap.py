import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from  fastSPD import Battle
   
fig = plt.figure()

"""    
for i in range(1, Battle.num_ens+1):
    df = pd.read_csv('output{}.csv'.format(i)) 
    df_pivot = df.pivot('Dg','Dr', 'Fraction of Cooperation')
      
    ax = fig.add_subplot(2, 5, i)
    sns.heatmap(df_pivot, 
                vmin = 0.0, vmax = 1.0, 
                annot = False, 
                cbar = False,
                cmap="jet",
                square = False)
          
    plt.gca().invert_yaxis()
    ax.set_title("Episode{}".format(i))

plt.tight_layout()
fig.suptitle('Fraction of Cooperation', fontsize=16)
#plt.subplots_adjust(top=1.0)
"""

df = pd.read_csv('output1.csv') 
df_pivot = df.pivot('Dg','Dr', 'Fraction of Cooperation')
sns.heatmap(df_pivot, 
            vmin = 0.0, vmax = 1.0, 
            annot = True, 
            cbar = True,
            cmap="jet",
            square = False)
plt.gca().invert_yaxis()
plt.title('Fraction of Cooperation') 
plt.show()
#fig.savefig('Fc.png')
