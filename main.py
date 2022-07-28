#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from simulation import Simulation
import random

def main():
    population = 100            # Agent number
    average_degree = 8          # Average degree of social network
    num_episode = 2             # Number of total episode in a single simulation for taking ensemble average
    network_type = "lattice"    # topology of social network
    display_transparency = 0.7
    simulation = Simulation(population, average_degree, network_type,display_transparency)

    for episode in range(num_episode):
        random.seed()
        simulation.one_episode(episode)

if __name__ == '__main__':
    main()
