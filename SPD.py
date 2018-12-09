#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import random as rnd
import networkx as nx
import csv
import matplotlib.pyplot as plt

class Agent:
    
    def __init__(self, id):
        self.id = id
        self.point = 0.0
        self.strategy = "D"
        self.next_strategy = None
        self.neighbors_id = []

class Society(Agent):
    
    def __init__(self, population_size, average_degree, network_type):
        """
        network_type has several options, give following network type as string;
            1. lattice
            2. ring
            3. ER-random
            4. Complete (Not recommended!!! Too heavy!!!)
            4. Watts Strogatz(Small World)
            5. BA-SF
        """
        
        rearange_edges = int(average_degree*0.5)
        self.size = population_size
        self.network_type = network_type
        
        if self.network_type == "lattice":
            self.topology = self.generate_lattice(population_size)
            
        if self.network_type == "ring":
            self.topology = nx.circulant_graph(population_size, [1])
            
        if self.network_type == "ER":
            self.topology = nx.random_regular_graph(average_degree, population_size)
        
        if self.network_type == "Complete":
            self.topology = nx.complete_graph(population_size)
            
        if self.network_type == "WS":
            self.topology = nx.watts_strogatz_graph(population_size, average_degree, 0.5)
        
        if self.network_type == "BA-SF":
            self.topology = nx.barabasi_albert_graph(self.size, rearange_edges)
            
        self.agents = self.generate_agents()
    
    def generate_lattice(self, population_size):
        """
        Default Lattice has only 4 adges(vertical&horizontal), so adding 4 edges in diagonal direction and 
        Set periodic boundary condition
        """

        n = int(np.sqrt(population_size))    # n×n lattice is generated
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
        
        if self.network_type == "lattice":
            n = int(np.sqrt(self.size))      
            for focal in agents:
                neighbors_id = list(self.topology[int(focal.id//n), int(focal.id%n)])
                for (x,y) in neighbors_id:
                    nb_id = int(x*n+y)
                    focal.neighbors_id.append(nb_id)

        # When using another topology
        else:    
            for focal in agents:
                neighbors_id = list(self.topology[focal.id])
                for nb_id in neighbors_id:
                    focal.neighbors_id.append(nb_id)
                
        return agents

    def generate_agents(self):
        """Generate a list of agents connected with network"""
        
        agents = [Agent(id) for id in range(self.size)]
        agents = self.connect_agents(agents)
        
        return agents
    
    def count_fraction(self):
        """Calculate the fraction of cooperative agents"""
        
        Fc = len([agent for agent in self.agents if agent.strategy == "C"])/self.size
    
        return Fc

    def snapshot(self, t):
        if self.network_type == "lattice":
            n = int(np.sqrt(self.size))
            for focal in self.agents:
                if focal.strategy == "C":
                    self.topology.nodes[int(focal.id//n), int(focal.id%n)]["strategy"] = "C"
                else:
                    self.topology.nodes[int(focal.id//n), int(focal.id%n)]["strategy"] = "D"                
                
            def color_for_lattice(i,j):
                if self.topology.nodes[i,j]["strategy"] == "C":
                    return 'cyan'
                else:
                    return 'pink'

            color = dict(((i, j), color_for_lattice(i,j)) for i,j in self.topology.nodes())
            pos = dict((n, n) for n in self.topology.nodes())   
        
        else:
            for focal in self.agents:
                if focal.strategy == "C":
                    self.topology.nodes[focal.id]["strategy"] = "C"
                else:
                    self.topology.nodes[focal.id]["strategy"] = "D"

            def color(i):
                if self.topology.nodes[i]["strategy"] == "C":
                    return 'cyan'
                else:
                    return 'pink'
            
            color =  dict((i, color(i)) for i in self.topology.nodes())
            if self.network_type == "ring":
                pos = nx.circular_layout(self.topology)

            else:
                pos = nx.spring_layout(self.topology)
                
        nx.draw_networkx_edges(self.topology, pos)
        nx.draw_networkx_nodes(self.topology, pos, node_color = list(color.values()), node_size = 10)
        plt.title('t={}'.format(t), fontsize=20)
        plt.xticks([])
        plt.yticks([])
        plt.savefig('snapshot_t={}.png'.format(format(t, '.1f')))
        plt.close()
        
class Decision:
    
    def __init__(self, Dg, Dr, beta):
        self.Dg = Dg
        self.Dr = Dr
        self.kappa = 1/beta   # Thermal coefficient for Pairwise Fermi update

    def choose_init_c(num_agent):
        """Return the ID list of initial C agent"""

        init_c = [id for id in rnd.sample(range(num_agent), k= int(num_agent/2))]

        return init_c

    def init_strategy(self, agents, init_c):
        """Initialize the strategy of agents"""

        for focal in agents:
            if focal.id in init_c:
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
            for neighbor_id in focal.neighbors_id:
                if focal.strategy == "C" and agents[neighbor_id].strategy == "C":    
                    focal.point += R 
                if focal.strategy == "C" and agents[neighbor_id].strategy == "D":   
                    focal.point += S
                if focal.strategy == "D" and agents[neighbor_id].strategy == "C":   
                    focal.point += T
                if focal.strategy == "D" and agents[neighbor_id].strategy == "D":  
                    focal.point += P

        return agents

    def Imitation_Max(self, agents):
        """Decide next strategy by Imitation-Max rule"""
        for focal in agents:
            neighbors_point = [agents[neighbor_id].point for neighbor_id in focal.neighbors_id]
            best_neighbor_id = focal.neighbors_id[np.argmax(neighbors_point)]
            best_neighbor = agents[best_neighbor_id]

            if focal.point < best_neighbor.point:
                focal.next_strategy = best_neighbor.strategy
            else:
                focal.next_strategy = focal.strategy
                
        return agents
    
    def PW_Fermi(self, agents): 
        """Decide next strategy by Pairwise-Fermi rule"""
        
        for focal in agents:
            opp_id = rnd.choice(focal.neighbors_id)   # Choose opponent from neighbors
            opp = agents[opp_id]
            if opp.strategy != focal.strategy and rnd.random() < 1/(1+np.exp((focal.point - opp.point)/kappa)):
                focal.next_strategy = opp.strategy
            else:
                focal.next_strategy = focal.strategy

        return agents

    def update_strategy(self, agents):
        """Insert next_strategy into current strategy"""
        
        #agents = self.Imitation_Max(self.payoff(agents))
        agents = self.PW_Fermi(self.payoff(agents))
        for focal in agents:
            focal.strategy = focal.next_strategy

        return agents

def main():
    num_agent = 10000      # Agent number
    average_degree = 8     # Average degree of social network
    num_play = 1000        # Number of maximum timestep in a single episode
    num_ens = 100          # Number of total episode in a single simulation for taking ensemble average
    beta = 10              # Inverse temperature(1/kappa) for Pairwise-Fermi update
    
    society = Society(num_agent, average_degree, "lattice")

    for ens in range(num_ens):
        rnd.seed()
        init_c = Decision.choose_init_c(society.size)
        
        # Setting for drawing Dg-Dr phase diagram
        # Can be plotted by heatmap.py
        filename1 = f"phase_diagram{ens}.csv"
        f1 = open(filename1, "w")      
        header1 = ["Dg", "Dr", "Fc"]
        writer1 = csv.writer(f1)
        writer1.writerow(header1)
        
        for Dr in np.arange(0, 1.1, 0.1):
            for Dg in np.arange(0, 1.1, 0.1):
                
                # Setting for drawing the time evolution of Fc
                # Can be plotted with time_evolution_dilemma_loop.py and time_evolution.py
                filename2 = f"time_evolution_Dg_{Dg:.1f}_Dr_{Dr:.1f}.csv"   # When drawing time evolution on different Dg in a single episode 
                f2 = open(filename2, "w")
                header2 = ["time", "Fc"]
                writer2 = csv.writer(f2)
                writer2.writerow(header2)
            
                ############################## Initialization ###############################
                decision = Decision(Dg, Dr, beta)
                society.agents = decision.init_strategy(society.agents, init_c)
                initFc = society.count_fraction()
                Fc = [initFc]
                print(f"Episode:{ens}, Dr:{Dr:.2f}, Dg:{Dg:.2f}, Time:{0}, Fc:{Fc[0]:.3f}")
                #society.snapshot(0)
                writer2.writerow([1, f'{Fc[0]:.3f}'])
                ############################# END Initialization ############################
                
                ############################# Time evolution loop ###############################
                for t in range(1, num_play+1):
                    society.agents = decision.update_strategy(society.agents)
                    Fc.append(society.count_fraction())
                    print(f"Episode:{ens}, Dr:{Dr:.1f}, Dg:{Dg:.1f}, Time:{t}, Fc:{Fc[t]:.3f}")
                    #society.snapshot(t)
                    writer2.writerow([t, f"{Fc[t-1]:.3f}"])
                    
                    """Following if statements are convergence conditions"""
                    if Fc[t] == 0 or Fc[t] == 1:
                        print(f"Dr:{Dr:.1f}, Dg:{Dg:.1f}, Time:{t}, Fc(0 or 1):{Fc[t]:.3f}")
                        writer1.writerow([f"{Dr:.1f}", f"{Dg:.1f}", f"{Fc[t-1]:.3f}"])
                        break

                    if t >= 100:
                        if np.absolute(np.mean(Fc[t-100:t-1]) - Fc[t])/Fc[t] < 0.001:
                            print(f"Dr:{Dr:.1f}, Dg:{Dg:.1f}, Time:{t}, Fc(Converged):{Fc[t]: .3f}")
                            writer1.writerow([f"{Dr:.1f}", f"{Dg:.1f}", f"{Fc[t-1]:.3f}"])
                            break

                    if t == num_play:
                        FcFin = np.mean(Fc[t-99:t])
                        print(f"Dr:{Dr:.1f}, Dg:{Dg:.1f}, Time:{t}, Fc(Final timestep):{FcFin:.3f}")
                        writer1.writerow([f"{Dr:.1f}", f"{Dg:.1f}", f"{FcFin:.3f}"])
                        break
                 ########################### END Time evolution loop ############################
                
                f2.close()
        f1.close()
if __name__ == '__main__':
    main()
