import numpy as np
import random as rnd
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from agent import Agent

class Simulation:
    
    def __init__(self, population, average_degree, network_type):
        """
        network_type has several options, give following network type as string;
            1. lattice
            2. ring
            3. ER-random
            4. Complete (Not recommended!!! Too heavy!!!)
            4. Watts Strogatz(Small World)
            5. BA-SF
        """

        self.network_type = network_type
        self.network = None
        self.agents = self.__generate_agents(population, average_degree)
        self.initial_cooperators = self.__choose_initial_cooperators()

    def __generate_agents(self, population, average_degree):
        if self.network_type == "lattice":
            self.network = self.__generate_lattice(population)
            
        elif self.network_type == "ring":
            self.network = nx.circulant_graph(population, [1])
            
        elif self.network_type == "ER":
            self.network = nx.random_regular_graph(average_degree, population)
        
        elif self.network_type == "Complete":
            self.network = nx.complete_graph(population)
            
        elif self.network_type == "WS":
            self.network = nx.watts_strogatz_graph(population, average_degree, 0.5)
        
        elif self.network_type == "BA-SF":
            rearange_edges = int(average_degree*0.5)
            self.network = nx.barabasi_albert_graph(population, rearange_edges)

        agents = [Agent() for id in range(population)]

        if self.network_type == "lattice":
            n = int(np.sqrt(population))   
            for index, focal in enumerate(agents):
                neighbors_id = list(self.network[int(index//n), int(index%n)])
                for (x,y) in neighbors_id:
                    nb_id = int(x*n+y)
                    focal.neighbors_id.append(nb_id)

        # When using another topology
        else:
            for index, focal in enumerate(agents):
                neighbors_id = list(self.network[index])
                for nb_id in neighbors_id:
                    focal.neighbors_id.append(nb_id)
        
        return agents

    def __generate_lattice(self, population):
        """
        Default Lattice has only 4 adges(vertical&horizontal), so adding 4 edges in diagonal direction and 
        Set periodic boundary condition
        """

        n = int(np.sqrt(population))    # n×n lattice is generated
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

    def __choose_initial_cooperators(self):
        population = len(self.agents)
        self.initial_cooperators = rnd.sample(range(population), k = int(population/2))

    def __initialize_strategy(self):
        """Initialize the strategy of agents"""

        for index, focal in enumerate(self.agents):
            if index in self.initial_cooperators:
                focal.strategy = "C"
            else:
                focal.strategy = "D"

    def __count_payoff(self, Dg, Dr):
        """Count the payoff based on payoff matrix"""

        R = 1       # Reward
        S = -Dr     # Sucker
        T = 1+Dg    # Temptation
        P = 0       # Punishment

        for focal in self.agents:
            focal.point = 0.0
            for nb_id in focal.neighbors_id:
                neighbor = self.agents[nb_id]
                if focal.strategy == "C" and neighbor.strategy == "C":    
                    focal.point += R 
                elif focal.strategy == "C" and neighbor.strategy == "D":   
                    focal.point += S
                elif focal.strategy == "D" and neighbor.strategy == "C":   
                    focal.point += T
                elif focal.strategy == "D" and neighbor.strategy == "D":  
                    focal.point += P

    def __update_strategy(self, rule = "IM"):
        for focal in self.agents:
            focal.decide_next_strategy(self.agents, rule = rule)
        
        for focal in self.agents:
            focal.update_strategy()

    def __count_fc(self):
        """Calculate the fraction of cooperative agents"""
        
        fc = len([agent for agent in self.agents if agent.strategy == "C"])/len(self.agents)
    
        return fc

    def __play_game(self, episode, Dg, Dr):
        """Continue games until fc gets converged"""
        tmax = 3000

        self.__initialize_strategy()
        initial_fc = self.__count_fc()
        fc_hist = [initial_fc]
        print(f"Episode:{episode}, Dr:{Dr:.1f}, Dg:{Dg:.1f}, Time: 0, Fc:{initial_fc:.3f}")
        # result = pd.DataFrame({'Time': [0], 'Fc': [initial_fc]})

        for t in range(1, tmax+1):
            self.__count_payoff(Dg, Dr)
            self.__update_strategy(rule = "IM")
            fc = self.__count_fc()
            fc_hist.append(fc)
            print(f"Episode:{episode}, Dr:{Dr:.1f}, Dg:{Dg:.1f}, Time:{t}, Fc:{fc:.3f}")
            # new_result = pd.DataFrame([[t, fc]], columns = ['Time', 'Fc'])
            # result = result.append(new_result)

            # Convergence conditions
            if fc == 0 or fc == 1:
                fc_converged = fc
                comment = "Fc(0 or 1"
                break

            if t >= 100 and np.absolute(np.mean(fc_hist[t-100:t-1]) - fc)/fc < 0.001:
                fc_converged = np.mean(fc_hist[t-99:t])
                comment = "Fc(converged)"
                break

            if t == tmax:
                fc_converged = np.mean(fc_hist[t-99:t])
                comment = "Fc(final timestep)"
                break

        print(f"Dr:{Dr:.1f}, Dg:{Dg:.1f}, Time:{t}, {comment}:{fc_converged:.3f}")
        # result.to_csv(f"time_evolution_Dg_{Dg:.1f}_Dr_{Dr:.1f}.csv")

        return fc_converged

    def __take_snapshot(self, timestep):
        if self.network_type == "lattice":
            n = int(np.sqrt(len(self.agents)))
            for index, focal in enumerate(self.agents):
                if focal.strategy == "C":
                    self.network.nodes[int(index//n), int(index%n)]["strategy"] = "C"
                else:
                    self.network.nodes[int(index//n), int(index%n)]["strategy"] = "D"                
                
            def color_for_lattice(i,j):
                if self.network.nodes[i,j]["strategy"] == "C":
                    return 'cyan'
                else:
                    return 'pink'

            color = dict(((i, j), color_for_lattice(i,j)) for i,j in self.network.nodes())
            pos = dict((n, n) for n in self.network.nodes())
        
        else:
            for index, focal in enumerate(self.agents):
                if focal.strategy == "C":
                    self.network.nodes[index]["strategy"] = "C"
                else:
                    self.network.nodes[index]["strategy"] = "D"

            def color(i):
                if self.network.nodes[i]["strategy"] == "C":
                    return 'cyan'
                else:
                    return 'pink'
            
            color =  dict((i, color(i)) for i in self.network.nodes())
            if self.network_type == "ring":
                pos = nx.circular_layout(self.network)

            else:
                pos = nx.spring_layout(self.network)
                
        nx.draw_networkx_edges(self.network, pos)
        nx.draw_networkx_nodes(self.network, pos, node_color = list(color.values()), node_size = 10)
        plt.title('t={}'.format(timestep), fontsize=20)
        plt.xticks([])
        plt.yticks([])
        plt.savefig(f"snapshot_t={timestep}.png")
        plt.close()

    def one_episode(self, episode):
        """Run one episode"""

        result = pd.DataFrame({'Dg': [], 'Dr': [], 'Fc': []})
        self.__choose_initial_cooperators()

        for Dr in np.arange(0, 1.1, 0.1):
            for Dg in np.arange(0, 1.1, 0.1):
                fc_converged = self.__play_game(episode, Dg, Dr)
                new_result = pd.DataFrame([[format(Dg, '.1f'), format(Dr, '.1f'), fc_converged]], columns = ['Dg', 'Dr', 'Fc'])
                result = result.append(new_result)
        
        result.to_csv(f"phase_diagram{episode}.csv")