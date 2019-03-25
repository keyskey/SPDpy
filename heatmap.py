import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

def draw_heatmap(pivot_table):
    sns.heatmap(pivot_table, 
                vmin = 0.0, 
                vmax = 1.0, 
                annot = False, 
                cbar = False,
                cmap ="jet",
                square = True,
                xticklabels = 2,
                yticklabels = 2)

num_episode = int(sys.argv[1])  # Number of simulation episodes
fig = plt.figure(figsize = (14, 8))

# If you have a result of many episodes
if num_episode > 1:
    for i in range(num_episode):
        df = pd.read_csv(f"phase_diagram{i}.csv")
        df_pivot = df.pivot('Dg','Dr', 'Fc')
        ax = fig.add_subplot(2, 5, i+1)
        draw_heatmap(df_pivot)
        plt.gca().invert_yaxis()
        ax.set_title(f"Episode{i}")
    
    plt.tight_layout()
    fig.suptitle('Fraction of Cooperation', fontsize=16)

# If you have a result of one episodes
elif num_episode == 1:
    df = pd.read_csv(f"phase_diagram0.csv")
    df_pivot = df.pivot('Dg','Dr', 'Fc')
    draw_heatmap(df_pivot)
    plt.gca().invert_yaxis()
    plt.title('Fraction of Cooperation') 

plt.show()
fig.savefig('Dg-Dr-Diagram.png')
