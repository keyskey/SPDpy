import matplotlib.pyplot as plt
import networkx as nx

C = 1
D = 0

def snapshot(G, agent_list, t):
    # Function for drawing snapshot of the spatial distribution of C/D agents
    # Pay attention to the network topology!!
    
    for focal in agent_list:
        if focal.strategy == C:
            G.nodes[int(focal.id//n), int(focal.id%n)]['strategy'] = C                # Lattice
            #G.nodes[focal.id]['strategy'] = C                                        # Other topology

        else:
            G.nodes[int(focal.id//n), int(focal.id%n)]['strategy'] = D                # Lattice
            #G.nodes[focal.id]['strategy'] = D                                        # Other topology

    def color(i,j):                                                                   # Lattice
    #def color(i):                                                                    # Other topology
        if G.nodes[i,j]['strategy'] == C:                                             # Lattice 
        #if G.nodes[i]['strategy'] ==C:                                               # Other topology
            return 'blue'
        else:
            return 'red'

    color = dict(((i, j), color(i,j)) for i,j in G.nodes())    # Lattice
    pos = dict((n, n) for n in G.nodes())   
    
    #color =  dict((i, color(i)) for i in G.nodes())           # Other topology
    #pos = nx.spring_layout(G)

    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_nodes(G, pos, node_color = list(color.values()), node_size = 10)
    plt.savefig('snapshot_t={}.png'.format(format(t, '.1f')))
