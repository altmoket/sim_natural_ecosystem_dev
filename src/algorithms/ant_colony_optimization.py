from ..components import *
from collections import defaultdict
import math

class AntColony(object):
    def __init__(self, decay, alpha=1, beta=0.5, delta_tau = 0.6):      
        #self.pheromones: dict[Specie,dict[Zone,dict[Zone,int]]]= defaultdict({zone:{next:0 for next in adj} for zone,adj in adj_z})
        self.pheromones = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : (0,0))))
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.delta_tau = delta_tau
        #self.distances : dict[Zone,dict[Zone,int]]=defaultdict(lambda : defaultdict(int)) 

    def pick_move(self,animal,state):
        time,zone = state
        if self.Is_goal(animal,zone):
            animal.path.append(zone)
            self.spread_pheronome(time,animal)
            animal.path=[]
            return zone
        else:
            max=0
            choice=None
            for next_zone,distance in zone.adj_z.items():
                if not next_zone in animal.path:
                    pheromones,last_time=self.pheromones[type(animal)][zone][next_zone]
                    real_pheromones=((1-self.decay)**(time-last_time))*pheromones
                    weight=self.get_probability(real_pheromones,distance)
                    if weight>=max:
                        max=weight
                        choice=next_zone
            if choice == None: return None
            animal.path.append(choice)
            return choice

    def spread_pheronome(self,time,animal):
        zone = animal.path[0]
        for next_zone in animal.path[1:]:
            pheromones,last_time=self.pheromones[type(animal)][zone][next_zone]
            real_pheromones=((1-self.decay)**(time-last_time))*pheromones
            self.pheromones[type(animal)][zone][next_zone]=(real_pheromones + self.delta_tau,time)
            zone=next_zone

    def get_probability(self,pheromones,distance):
        return math.pow(pheromones,self.alpha)+math.pow(1/distance,self.beta)
    
    def Is_goal(self,animal,zone):
        if zone.vegetation > 0 and type(animal).feed_on_vegetation()>0: return True
        can_eat=lambda item: item[0] in type(animal).prey() and len(item[1][0]+item[1][1])>0
        return len(list(filter(can_eat,zone.species.items()))) > 0
    