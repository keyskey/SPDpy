import random as rnd
import numpy as np

class Agent:
    
    def __init__(self):
        self.point = 0.0
        self.strategy = None
        self.next_strategy = None
        self.neighbors_id = []

    def __imitation_max(self, agents):
        neighbors_point = [agents[neighbor_id].point for neighbor_id in self.neighbors_id]
        best_neighbor_id = self.neighbors_id[np.argmax(neighbors_point)]
        best_neighbor = agents[best_neighbor_id]

        if self.point < best_neighbor.point:
            self.next_strategy = best_neighbor.strategy
        else:
            self.next_strategy = self.strategy

    def __pairwise_fermi(self, agents):
        opp_id = rnd.choice(self.neighbors_id)   # Choose opponent from neighbors
        opp = agents[opp_id]

        if opp.strategy != self.strategy and rnd.random() < 1/(1 + np.exp((self.point - opp.point)/0.1)):
            self.next_strategy = opp.strategy
        else:
            self.next_strategy = self.strategy

    def decide_next_strategy(self, agents, rule):
        """
        rule = "IM" or "PF" 
        """
        if rule == "IM":
            self.__imitation_max(agents)

        elif rule == "PF":
            self.__pairwise_fermi(agents)

    def update_strategy(self):
        self.strategy = self.next_strategy