import random as rn
import numpy as np
from numpy.random import choice as np_choice
from ..components import *
from collections import defaultdict

class AntColony(object):

    def __init__(self, zone:Zone,adj_z:list[Zone,list[Zone]], decay, alpha=1, beta=0.5, delta_tau = 2, ):
        self.zone=zone
        self.adj_z  = adj_z
        self.pheromone = self.get_pheromone()
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.delta_tau = delta_tau
        self.all_time_shortest_path = (-1, "placeholder", np.inf)
        self.distance = self.get_pheromone()

    def get_pheromone(self):
        pheromone=np.zeros((len(self.adj_z),len(self.adj_z)))
        pheromone=np.fill_diagonal(pheromone,-1)

    def run(self,n_ants,n_iterations):
        shortest_path = None
        
        for i in range(n_iterations):
            all_paths = self.gen_all_paths(n_ants)
            self.spread_pheronome(all_paths)
            shortest_path = min(all_paths, key=lambda x: x[1])
            
            if shortest_path[1] < self.all_time_shortest_path[2]:
                self.all_time_shortest_path = (i, *shortest_path)
                
            #if i%10==0: print(i,  "mean: ", mean([path[1] for path in all_paths]), "best_iteration_solution: ", shortest_path ,"best_global_solution: ", all_time_shortest_path)
            
        return self.all_time_shortest_path

    def spread_pheronome(self, all_paths):
        #TODO: Your code here!
        return None

    def path_dist(self, path):
        #TODO: Your code here!
        return None

    def gen_all_paths(self,n_ants):
        all_paths = []
        for i in range(n_ants):
            visited=np.zeros(len(self.zone))
            path = self.gen_path(self.zone,visited)
            all_paths.append((path, self.path_dist(path)))
        return all_paths

    def gen_path(self,zone,visited,distance):
        for next_zone in self.adj_z[zone]:
            if not visited[next_zone]:
                visited[next_zone]=True
                distance[next_zone]=min(distance[next_zone],distance[zone]+1)
        return None

    def pick_move(self, pheromone, dist, visited):
        #TODO: Your code here!
        return None
    
    def evaporate_pheromone(self):
        #TODO: Your code here!
        return None    