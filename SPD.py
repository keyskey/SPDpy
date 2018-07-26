# coding: utf-8
import numpy as np
import random as rnd
import networkx as nx
import csv
from snapshot import snapshot

N = 10000              # Agent number
n = int(np.sqrt(N))    # In case of lattice topology, n×n grid is generated
kappa = 0.1            # Thermal coefficient for Pairwise Fermi update
C = 1                  # C: Cooperation
D = 0                  # D: Defection

num_play = 1000        # Number of total timestep in a single senario
num_ens = 1            # Number of total episode in a single simulation for taking ensemble average

class Agent:
    # Define agent object
    
    def __init__(self, id):
        self.id = id
        self.point = 0.0
        self.strategy = D
        self.next_strategy = None 
        self.neighbors = []
        self.neighbors_id = None        

    def update_strategy(self):
        self.strategy = self.next_strategy

   
def network(agent_list):
    # Generate network and set neighbors
    
    G = nx.grid_graph(dim = [n,n])             # Default Lattice has only 4 adges(vertical&horizontal), so adding 4 edges(diagonal)
    #G = nx.random_regular_graph(d, N)         # random_regular_graph(d,n)  d:degree, n:node number 
    #G = nx.barabasi_albert_graph(N,m)         # barabasi_albert_graph(n,m)   n:node number, m: number of edges to rearange

    # Add diagonal edge except for outer edge agent
    for i in range(1,n-1):
        for j in range(1,n-1):
            G.add_edge((i,j), (i+1,j+1))
            G.add_edge((i,j), (i+1,j-1))
            G.add_edge((i,j), (i-1,j+1))
            G.add_edge((i,j), (i-1,j-1))
            
    # Add edge along i = 0, j=1~n-2
    for j in range(1,n-1):
        G.add_edge((0,j), (n-1,j))
        G.add_edge((0,j), (n-1,j+1))
        G.add_edge((0,j), (n-1,j-1))
        G.add_edge((0,j), (1,j-1))
        G.add_edge((0,j), (1,j+1))
        
    # Add edge along j=0, i=1~n-2
    for i in range(1,n-1): 
        G.add_edge((i,0), (i,n-1))
        G.add_edge((i,0), (i-1,n-1))
        G.add_edge((i,0), (i+1,n-1))
        G.add_edge((i,0), (i+1,1))
    
    # Add edge along j=0
    G.add_edge((0,0), (n-1,0))
    G.add_edge((0,0), (n-1,0+1))
    G.add_edge((0,0), (n-1,n-1))
    G.add_edge((0,0), (0,n-1))
    G.add_edge((0,0), (1,n-1))
  
    # Add edge along j=n-1
    G.add_edge((0,n-1), (n-1,n-1))
    G.add_edge((0,n-1), (n-1,0))
    G.add_edge((0,n-1), (n-1,n-2))
    G.add_edge((0,n-1), (0,0))
    
    # Add edge along i=n-1
    G.add_edge((n-1,0), (0,0))
    G.add_edge((n-1,0), (0,1))
    G.add_edge((n-1,0), (0,n-1))
    G.add_edge((n-1,0), (n-1,n-1))
    G.add_edge((n-1,0), (n-2,n-1))
           
    # Upper right edge agent
    G.add_edge((n-1,n-2),(n-2,n-1))

    # Set neighbors to all agents
    for focal in agent_list:
        focal.neighbors_id = list(G[int(focal.id//n), int(focal.id%n)])             # Lattice    
        #focal.neighbors_id = list(G[focal.id])                                     # Other topology
        
        for neighbor in agent_list:
            if (int(neighbor.id//n), int(neighbor.id%n)) in focal.neighbors_id:     # Lattice
            #if neighbor.id in focal.neighbors_id:                                  # Other topology
                focal.neighbors.append(neighbor)    
                
    return G

def initialize(agent_list, init_C):
    # Initialize the strategy of all agents
    
    for agent in agent_list:
        if agent.id in init_C:
            agent.strategy = C
        else:
            agent.strategy = D

def payoff(Dg, Dr, agent_list):
    # Count the payoff based on payoff matrix
    
    R = 1       # Reward
    S = -Dr     # Sucker
    T = 1+Dg    # Temptation
    P = 0       # Punishment

    for focal in agent_list:
        focal.point = 0.0
       
        for neighbor in focal.neighbors:
      
            if focal.strategy == C and neighbor.strategy == C:    
                focal.point += R 
            
            if focal.strategy == C and neighbor.strategy == D:   
                focal.point += S
      
            if focal.strategy == D and neighbor.strategy == C:   
                focal.point += T

            if focal.strategy == D and neighbor.strategy == D:  
                focal.point += P
                
def IM_update(agent_list):
    # Strategy update by Imitation-Max rule
    
    for focal in agent_list:
        points = [i.point for i in focal.neighbors]
        best = focal.neighbors[np.argmax(points)]
        
        if focal.point < best.point:
            focal.next_strategy = best.strategy
        else:
            focal.next_strategy = focal.strategy

    for focal in agent_list:
        focal.update_strategy()

def PF_update(agent_list):
    # Strategy update by Pairwise-Fermi rule
    
    for focal in agent_list:
        opp = rnd.choice(focal.neighbors)
        if opp.strategy != focal.strategy:
            if rnd.random() <= 1/(1+np.exp((focal.point - opp.point)/kappa)):
               focal.next_strategy = opp.strategy
            else:
               focal.next_strategy = focal.strategy
        else:
            focal.next_strategy = focal.strategy
    for focal in agent_list:
        focal.update_strategy()
 
def count(agent_list):
    # Count the number of cooperative agent and get the fraction of cooperation(=Fc)
    
    Fc = len(list(filter(lambda agent: agent.strategy == C, agent_list)))/N
    
    return Fc

def main():

    agent_list = [Agent(id) for id in range(N)]
    G = network(agent_list)

    # Ensamble loop
    for ens in range(1, num_ens+1):

        # Reset the seed of random number                                   
        rnd.seed()

        # Determine initial C agent over one episode
        init_C = [id for id in rnd.sample(range(N), k= int(N/2))]
         
        # Setting for drawing Dg-Dr diagram
        # Output file can be plotted with heatmap.py
        filename1 = 'output{}.csv'.format(ens)
        f1 = open(filename1, 'w')        
        header1 = ['Dg', 'Dr', 'Fraction of Cooperation']
        writer1 = csv.writer(f1)
        writer1.writerow(header1)

        # Dilemma strength loop
        for Dr in np.arange(0, 1.1, 0.1):          # Stag-Hunt type dilemma              
            for Dg in np.arange(0, 1.1, 0.1):      # Chicken type dilemma

                # Setting for drawing the time evolution of Fc
                # Can be plotted with time_evolution.py
                """
                filename2 = 'time_evolution(episode{}).csv'.format(ens)     # When drawing time evolution of many episodes for the same Dg
                #filename2 = 'time_evolution(Dg={}).csv'.format(Dg)         # When drawing time evolution on different Dg in a single episode 
                f2 = open(filename2, 'w')
                header2 = ['time', 'Fraction of Cooperation']
                writer2 = csv.writer(f2)
                writer2.writerow(header2)
                """
                
                # Initialization
                initialize(agent_list, init_C)
                initFc = count(agent_list)
                Fc = [initFc]
                print('Dg:{:0.1f}, Dr:{:0.1f}, Time:{}, Fc:{:0.3f}'.format(Dg, Dr, 0, Fc[0]))
                #snapshot(G, agent_list, 0)
                #writer2.writerow([0, format(Fc[0],'.3f')])    

       	        # Time evolution loop
                for t in range(1, num_play+1):
                    payoff(Dg, Dr, agent_list)
                    IM_update(agent_list)
                    #PF_update(agent_list)
                    Fc.append(count(agent_list))
                    print('Dg:{:0.1f}, Dr:{:0.1f}, Time:{}, Fc:{:0.3f}'.format(Dg, Dr, t, Fc[t]))
                    #writer2.writerow([t, format(Fc[t],'.3f')])

                    #if t in [10*i for i in range(num_play)]:     # Take snapshot every 10 timestep 
                        #snapshot(G, agent_list, t)
                        
                    # Following if statemants are the condition for finishing calculation
                    if Fc[t] == 0 or Fc[t] == 1:
                        print("Dg:{:0.1f}, Dr:{:0.1f}, Time:{}, Fc(0 or 1):{:0.3f}".format(Dg, Dr, t, Fc[t]))
                        writer1.writerow([format(Dg,'.1f'), format(Dr,'.1f'), format(Fc[t],'.3f')])
                        break
                        
                    if t >= 100:
                        if np.absolute(np.mean(Fc[t-100:t-1]) - Fc[t])/Fc[t] < 0.0005:
                            print("Dg:{:0.1f}, Dr:{:0.1f}, Time:{}, Fc:{:0.3f}".format(Dg, Dr, t, Fc[t]))
                            writer1.writerow([format(Dg,'.1f'), format(Dr,'.1f'), format(Fc[t],'.3f')])
                            break
                            
                    if t == num_play+1:
                        # If not converged, calculate (num_play - 1) times and get answer avereged over past 100 timestep
                        FcFin = np.mean(Fc[t-99:t])
                        print("Dg:{:0.1f}, Dr:{:0.1f}, Time:{}, Fc:{:0.3f}".format(Dg, Dr, t, FcFin))
                        writer1.writerow([format(Dg,'.1f'), format(Dr,'.1f'), format(FcFin,'.3f')])
                        break
                  
                #snapshot(G, agent_list, t)      # Take anap shot of final timestep
                
        f1.close()
        #f2.close()
         
if __name__ == '__main__':
    main()
