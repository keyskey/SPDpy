#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import random as rnd
import networkx as nx
import csv
from snapshot import snapshot

class Agent:
    """Define agent object"""
    
    def __init__(self, id):
        self.id = id
        self.point = 0.0
        self.strategy = "D"
        self.next_strategy = None 
        self.neighbors = []

class Society(Agent):
    """
    Store Agents and check the fraction of cooperative agents 
    """ 
    def __init__(self, population_size, average_degree):
        rearange_edges = int(average_degree*0.5)
        self.size = population_size
        self.use_lattice = True   # Set True when using lattice as a social network
        
        if self.use_lattice == True:
            self.topology = self.generate_lattice(self.size)
        else:
            self.topology = nx.barabasi_albert_graph(self.size, rearange_edges)
            
        self.agents = self.generate_agents()
    
    def generate_lattice(self, num_node):
        """
        Default Lattice has only 4 adges(vertical&horizontal), so adding 4 edges in diagonal direction and 
        Set periodic boundary condition
        """

        n = int(np.sqrt(num_node))    # n×n lattice is generated
        G = nx.grid_graph(dim = [n,n]) 

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
        
        return G
        
    def connect_agents(self, agents):
        """Link all agents based on the underlying network topology"""
        
        if self.use_lattice == True:
            n = int(np.sqrt(self.size))        
            for focal in agents:
                neighbors_id = list(self.topology[int(focal.id//n), int(focal.id%n)])
                for (x,y) in neighbors_id:
                    nb_id = int(x*n+y)
                    focal.neighbors.append(agents[nb_id])
        else:
            for focal in agents:
                neighbors_id = list(self.topology[focal.id])
                for nb_id in neighbors_id:
                    focal.neighbors.append(agents[nb_id])

        return agents

    def generate_agents(self):
        """Generate a list of agents connected with network"""
        
        agents = [Agent(id) for id in range(self.size)]
        connected_agents = self.connect_agents(agents)
        
        return connected_agents
    
    def count_fraction(self):
        """Calculate the fraction of cooperative agents"""
        
        Fc = len([agent for agent in self.agents if agent.strategy == "C"])/self.size
    
        return Fc        
        
class Decision:
    """Functions for game theoretical decision making"""
    
    def __init__(self, Dg, Dr):
        self.Dg = Dg
        self.Dr = Dr
        self.kappa = 0.1  # Thermal coefficient for Pairwise Fermi update

    def choose_initC(num_agent):
        """Return the ID list of initial C agent"""

        init_C = [id for id in rnd.sample(range(num_agent), k= int(num_agent/2))]

        return init_C

    def init_strategy(self, agents, init_C):
        """Initialize the strategy of agents"""

        for focal in agents:
            if focal.id in init_C:
                focal.strategy = "C"
            else:
                focal.strategy = "D"

        return agents

    def payoff(self, agents):
        """Count the payoff based on payoff matrix"""

        R = 1            # Reward
        S = -self.Dr     # Sucker
        T = 1+self.Dg    # Temptation
        P = 0            # Punishment

        for focal in agents:
            focal.point = 0.0

            for neighbor in focal.neighbors:
                if focal.strategy == "C" and neighbor.strategy == "C":    
                    focal.point += R 
                if focal.strategy == "C" and neighbor.strategy == "D":   
                    focal.point += S
                if focal.strategy == "D" and neighbor.strategy == "C":   
                    focal.point += T
                if focal.strategy == "D" and neighbor.strategy == "D":  
                    focal.point += P

        return agents

    def Imitation_Max(self, agents):
        """Decide next strategy by Imitation-Max rule"""
        
        for focal in agents:
            points = [neighbor.point for neighbor in focal.neighbors]
            best_neighbor = focal.neighbors[np.argmax(points)]
        
            if focal.point < best_neighbor.point:
                focal.next_strategy = best_neighbor.strategy
            else:
                focal.next_strategy = focal.strategy
                
        return agents
    
    def PW_Fermi(self, agents): 
        """Decide next strategy by Pairwise-Fermi rule"""
        
        for focal in agents:
            opp = rnd.choice(focal.neighbors)   # Choose opponent from neighbors
            if opp.strategy != focal.strategy and rnd.random() <= 1/(1+np.exp((focal.point - opp.point)/self.kappa)):
                focal.next_strategy = opp.strategy
            else:
                focal.next_strategy = focal.strategy

        return agents

    def update_strategy(self, agents):
        """Insert next_strategy into current strategy"""
        
        agents = self.Imitation_Max(self.payoff(agents))

        for focal in agents:
            focal.strategy = focal.next_strategy

        return agents

def main():
    num_agent = 10000      # Agent number
    average_degree = 8     # Average degree of social network
    num_play = 1000        # Number of total timestep in a single episode
    num_ens = 100          # Number of total episode in a single simulation for taking ensemble average

    society = Society(num_agent, average_degree)
    
    # Ensemble loop
    for ens in range(1, num_ens+1):
        
        # Setting for drawing Dg-Dr diagram
        # Output file can be plotted with heatmap.py
        filename1 = f"output{ens}.csv"
        f1 = open(filename1, "w")        
        header1 = ["Dg", "Dr", "Fraction of Cooperation"]
        writer1 = csv.writer(f1)
        writer1.writerow(header1)

        # Reset the seed of random number                                   
        rnd.seed()

        # Determine initial C agent over one single episode
        init_C = Decision.choose_initC(num_agent)

        # Dilemma strength loop
        for Dr in np.arange(0, 1.1, 0.1):          # Stag-Hunt type dilemma              
            for Dg in np.arange(0, 1.1, 0.1):      # Chicken type dilemma
  
                # Setting for drawing the time evolution of Fc
                # Can be plotted with time_evolution_dilemma_loop.py and time_evolution.py
                """
                filename2 = f"time_evolution_Dg_{Dg:.1f}_Dr_{Dr:.1f}.csv"       # When drawing time evolution on different Dg in a single episode 
                f2 = open(filename2, "w")
                header2 = ["time", "Fraction of Cooperation"]
                writer2 = csv.writer(f2)
                writer2.writerow(header2)
                """
                
                ######################### Initialization #####################
                decision = Decision(Dg, Dr)
                society.agents = decision.init_strategy(society.agents, init_C)
                initFc = society.count_fraction()
                Fc = [initFc]
                print(f"Dg:{Dg:.1f}, Dr:{Dr:.1f}, Time:{0}, Fc:{Fc[0]:.3f}")
                #snapshot(society.topology, society.agents, 1)
                #writer2.writerow([1, f'{Fc[0]:.3f}'])
                ####################### End Initialization ####################
                
                ####################### Time evolution loop ###################
                for t in range(1, num_play+1):
                    society.agents = decision.update_strategy(society.agents)
                    Fc.append(society.count_fraction())
                    print(f"Dg:{Dg:.1f}, Dr:{Dr:.1f}, Time:{t}, Fc:{Fc[t]:.3f}")
                    #writer2.writerow([t, f"{Fc[t-1]:.3f}"])

                    #if t in [10*i for i in range(num_play)]:     # Take snapshots every 10 timesteps 
                        #snapshot(society.topology, society.agents, t)
                    
                    """Following if statements are convergence conditions"""
                    if Fc[t] == 0 or Fc[t] == 1:
                        print(f"Dg:{Dg:.1f}, Dr:{Dr:.1f}, Time:{t}, Fc(0 or 1):{Fc[t]: .3f}")
                        writer1.writerow([f"{Dg:.1f}", f"{Dr:.1f}", f"{Fc[t-1]:.3f}"])
                        break

                    if t >= 100:
                        if np.absolute(np.mean(Fc[t-100:t-1]) - Fc[t])/Fc[t] < 0.001:
                            print(f"Dg:{Dg:.1f}, Dr:{Dr:.1f}, Time:{t}, Fc(Converged):{Fc[t]: .3f}")
                            writer1.writerow([f"{Dg:.1f}", f"{Dr:.1f}", f"{Fc[t-1]:.3f}"])
                            break

                    if t == num_play:
                        FcFin = np.mean(Fc[t-99:t])
                        print(f"Dg:{Dg:.1f}, Dr:{Dr:.1f}, Time:{t}, Fc(Final timestep):{FcFin:.3f}")
                        writer1.writerow([f"{Dg:.1f}", f"{Dr:.1f}", f"{FcFin:.3f}"])
                        break
                ##################### End time evolution loop ##################
                
                #snapshot(society.topology, society.agents, t)      # Take the snapshot of final timestep
                #f2.close()
        f1.close()
if __name__ == '__main__':
    main()
