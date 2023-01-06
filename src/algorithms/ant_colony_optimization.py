import random as rn
import numpy as np
from numpy.random import choice as np_choice
from ..components import *
from collections import defaultdict
import math
class AntColony(object):

    def __init__(self, flock:Flock,adj_z:list[Zone,list[Zone]], decay, alpha=1, beta=0.5, delta_tau = 2 ):
        self.zone=flock.zone
        self.adj_z  = adj_z
        self.pheromone : dict[Zone,dict[Zone,int]]=defaultdict(lambda : defaultdict(int)) 
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.delta_tau = delta_tau
        self.all_time_shortest_path = (-1, "placeholder", np.inf)
        self.distances : dict[Zone,dict[Zone,int]]=defaultdict(lambda : defaultdict(int)) 

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
            for path in all_paths:
                for i in range(0,len(path)-2):
                    current=path[i]
                    next=path[i+1]
                    self.pheromone[current][next]+=self.delta_tau

    def path_dist(self, path):
        #TODO: Your code here!
        return None

    def gen_all_paths(self,n_ants):
        all_paths = []
        for i in range(n_ants):
            visited : defaultdict[Zone,bool] = defaultdict(lambda:False)
            path = self.gen_path(self.zone,visited)
            all_paths.append((path, self.path_dist(path)))
        return all_paths

    def gen_path(self,zone,visited,distance):
        for next_zone in self.adj_z[zone]:
            if not visited[next_zone]:
                visited[next_zone]=True
                distance[next_zone]=min(distance[next_zone],distance[zone]+1)
            result=self.gen_path(next_zone,visited,distance)
            if result:  return result 
        return None

    def probability(self,zone1,zone2):
        math.pow(self.pheromone[zone1][zone2],self.alpha)+math.pow(1/self.distances[zone1][zone2],self.beta)
    
    def Is_Objective(zone:Zone):
        return
    
    def evaporate_pheromone(self):
        #TODO: Your code here!
        return None    