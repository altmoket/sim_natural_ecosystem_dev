import random as rn
import numpy as np
from numpy.random import choice as np_choice
from ..components import *
from collections import defaultdict
import math
class AntColony(object):

    def __init__(self, decay, alpha=1, beta=0.5, delta_tau = 0.6):
        
        #self.pheromones: dict[Specie,dict[Zone,dict[Zone,int]]]= defaultdict({zone:{next:0 for next in adj} for zone,adj in adj_z})
        self.pheromones: dict[Specie,dict[Zone,dict[Zone,tuple(int,int)]]]= defaultdict(defaultdict(lambda : defaultdict(lambda : (0,0))))
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.delta_tau = delta_tau
        #self.distances : dict[Zone,dict[Zone,int]]=defaultdict(lambda : defaultdict(int)) 

    #def run(self,n_ants,n_iterations):
    #    shortest_path = None
        
    #    for i in range(n_iterations):
    #        all_paths = self.gen_all_paths(n_ants)
    #        self.spread_pheronome(all_paths)
    #        shortest_path = min(all_paths, key=lambda x: x[1])
            
    #        if shortest_path[1] < self.all_time_shortest_path[2]:
    #           self.all_time_shortest_path = (i, *shortest_path)
    #            
            #if i%10==0: print(i,  "mean: ", mean([path[1] for path in all_paths]), "best_iteration_solution: ", shortest_path ,"best_global_solution: ", all_time_shortest_path)
            
    #    return self.all_time_shortest_path

    def pick_move(self,animal:ReactiveAgent,state):
        time,zone:tuple[int,Zone]=state
        if self.Is_goal(animal,zone):
            animal.path.append(zone)
            self.spread_pheronome(time,animal)
            return zone
        else:
            max=0
            choice=None
            for next_zone,distance in zone.adj_z.items():
                if not next_zone in animal.path:
                    pheromones,last_time=self.pheromones[animal._type][zone][next_zone]
                    real_pheromones=((1-self.decay)**(time-last_time))*pheromones
                    weight=self.get_probability(real_pheromones,distance)
                    if weight>=max:
                        max=weight
                        choice=next_zone
            if choice == None: return None
            animal.path.append(choice)
            return choice
            

    def spread_pheronome(self,time,animal:ReactiveAgent):
        zone = animal.path[0]
        for next_zone in animal.path[1:]:
            pheromones,last_time=self.pheromones[animal._type][zone][next_zone]
            real_pheromones=((1-self.decay)**(time-last_time))*pheromones
            self.pheromones[animal._type][zone][next_zone][0]=real_pheromones + self.delta_tau
            self.pheromones[animal._type][zone][next_zone][1]=time
            zone=next_zone


    #def gen_all_paths(self,n_ants):
    #    all_paths = []
    #    for i in range(n_ants):
    #        visited : defaultdict[Zone,bool] = defaultdict(lambda:False)
    #        path = self.gen_path(self.zone,visited)
    #        all_paths.append((path, self.path_dist(path)))
    #    return all_paths

    #def gen_path(self,zone,visited,distance):
    #    for next_zone in self.adj_z[zone]:
    #        if not visited[next_zone]:
    #            visited[next_zone]=True
    #            distance[next_zone]=min(distance[next_zone],distance[zone]+1)
    #        result=self.gen_path(next_zone,visited,distance)
    #        if result:  return result 
    #    return None

    def get_probability(self,pheromones,distance):
        current=math.pow(pheromones,self.alpha)+math.pow(1/distance,self.beta)
    
    def Is_goal(self,animal:Species,zone:Zone):
        if zone.vegetation>0  and animal.feed_on_vegetation()>0: return True
        can_eat=lambda specie,animals: specie in animal.prey() and len(animals[0]+animals[1])>0
        return len(list(filter(can_eat,zone.species.items()))) > 0
    
    def evaporate_pheromone(self):
        #TODO: Your code here!
        return None    