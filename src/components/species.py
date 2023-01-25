from .utils import Habitat, Specie
import random
from ..algorithms import migration_astar, MigrationProblem

class Species:
    _type = Specie.base

    def __init__(self, sex: int):
        self.birthday = 0
        self.age = 0
        self.sex = sex
        self.health = round(random.uniform(92,100),3)
        self.full = round(random.uniform(92,100),3)
        self.time_death = random.randint(self.life_expectancy()[0], self.life_expectancy()[1])
        self.my_speed = random.randint(self.speed()[0], self.speed()[1])

    def habitat(self): raise NotImplementedError()
    def feed_on_vegetation(self): raise NotImplementedError()
    def life_expectancy(self): raise NotImplementedError()
    def speed(self): raise NotImplementedError()
    def prey(self): raise NotImplementedError()
    def depredator(self): raise NotImplementedError()
    def uninhabitable(self): raise NotImplementedError()
    def desnutrition(self): raise NotImplementedError()

class Agent(Species):
    def __init__(self, sex: int):
        Species.__init__(self, sex)
        self.path = []
        self.looking_for_food=False
        self.ate=False
        self.time_limb = 0
        self.is_starving = False
        self.feed_way='feed'
        self.migate_algorithm_1 = MigrationProblem()

    def reaction(self, state):    
        time, zone, colony = state
        if time == self.birthday: self.age += 1
        action = self.get_action(state)
        if action == 'death':
            zone.delete_animal(self)
        elif action == 'migrate':
            self.path[0].delete_animal(self)
            if 1- self.full/100 > 0.7: self.feed_here(self.path[0])
            self.path.pop(0)
            #distance:int = zone.adj_z[self.path[0]]
            #self.time_limb = max(1,distance // self.my_speed)
            self.time_limb = self.get_trip_time(zone,self.path[0])
            if len(self.path)>0 : self.path[0].limb.append((self, time))
        elif action == 'feed':
            self.feed_here(zone)
            if not self.ate:
                if not self.is_starving:
                    self.is_starving = True
                    next_zone, trip_time = self.get_next_zone(zone)
                    self.time_limb = trip_time
                    next_zone.limb.append((self,time))
                else: self.is_starving = False     
        elif action == 'look_for_food':
            next_zone=colony.pick_move(self,(time,zone))
            if next_zone == zone:
                self.looking_for_food=False
                self.feed_here(zone)
            elif next_zone == None: self.looking_for_food=False
            else:
                self.looking_for_food=True
                self.time_limb = self.get_trip_time(zone,next_zone)
                next_zone.limb.append((self,time))
        self.update(state)

    def get_action(self, state):
        if self.age == self.time_death: return 'death'
        if self.is_starving: return 'feed'
        if self.looking_for_food: return 'look_for_food'
        if len(self.path)>0 : return 'migrate'
        weight1 = self.feed_weight(state)
        path, weight2 = self.migrate_weight(state)
        if weight2 < 0.3 and  weight1 < 0.3: return 'nothing'
        if weight2 > weight1:
            self.path=path
            return 'migrate'
        return self.feed_way

    def update(self, state):
        time, zone = state
        hungry = 0 if self.ate else self.desnutrition()
        self.full = max(0, self.full - hungry)
        self.health = max(0, self.health - hungry - self.uninhabitable()[zone.type])
        if self.health == 0: return True
        if self.time_limb > 0:
            if time == self.birthday: self.age += 1
            if self.age == self.time_death: return True
            floor = 1 if zone.floor > 0 else 0
            self.time_limb = self.time_limb - 1 + floor
        self.ate = False

    def get_trip_time(self,zone,next_zone):
        distance:int = zone.adj_z[next_zone]
        time_limb = max(1,distance // self.my_speed)
        return time_limb

    def feed_here(self,zone):
        if self.feed_on_vegetation() > 0 and zone.vegetation > 0:
            zone.vegetation = max(0,zone.vegetation- self.feed_on_vegetation())
            self.full= min(100,self.full+self.feed_on_vegetation())
            self.ate = True
            self.is_starving=False
        else:
            for animal in self.prey():
                female,male=zone.species[animal]
                if len(female+male)>0: 
                    choice=random.choice(female+male)
                    zone.delete_animal(choice)
                    self.full= min(100,self.full+choice.full)
                    self.ate=True
                    self.is_starving=False
                    return 

    def get_next_zone(self, state):
        _ , zone , _ = state
        max = 0
        result=None
        time = 0
        for next_zone, distance in zone.adj_z.items():
            current =  next_zone.vegetation  if self.feed_on_vegetation() > 0 else 0 # vegetacion de la zona
            for animal in self.prey:
                current+= len(zone.species[animal][0])+len(zone.species[animal][1]) # cantidad de presas en la zona
            trip_time=max(1,distance//self.my_speed)
            current-= self.uninhabitable()[next_zone] * (trip_time) # nivel de salud que resta cruzar hacia la zona 
            for animal in self.depredator:
                current-= len(zone.species[animal][0])+len(zone.species[animal][1]) # cantidad de depredadores en la zona
            if result == None: 
                max=current
                result=next_zone
                time=trip_time
            elif current > max:
                max=current
                result=next_zone
                time=trip_time
            return result, time
 
    def feed_weight(self, state):
        result= self.full/100

    def migrate_weight(self, state):
        _,zone=state
        weight=0
        path=None
        if not zone.type in self.habitat:
            path = migration_astar(zone,zone.type,self.habitat_heuristic)
            if len(path)>0:
                current_weight = self.get_path_weight(path)
                if current_weight>0:
                    weight=current_weight
        depredators=list(filter(lambda specie : specie in self.prey(),zone.species.keys()))
        if len(depredators)>0:
            currentpath=migration_astar(zone,zone.type,self.depredator_heuristic)
            if len(currentpath)>0:
                current_weight=self.get_path_weight(path)
                if current_weight>0 and current_weight<=weight:
                    path = currentpath
        return path,weight

    def get_path_weight(self,path):
        health_left=self.health
        current_zone=path[0]
        for next_zone in path[1:]:
            time_limb = self.get_trip_time(current_zone,next_zone)
            health_left=max(0,health_left-time_limb * self.desnutrition())
        return health_left/100

    def depredator_heuristic(self, node): pass 
    def habitat_heuristic(self, node): pass 

class ReactiveAgent(Agent):
    def __init__(self, sex: int):
        Agent.__init__(self, sex)

    def habitat_heuristic(self, node):
        zone=node.state
        result=0
        for _, (female,male)  in zone.species.items():
            animals=female+male
            if len(animals)>0 and self.goal in animals[0].habitat():
                result+=len(animals)
        return zone.total - result

    def depredator_heuristic(self, node):
        zone=node.state
        result=0
        for _, (female,male)  in zone.species.items():
            animals=female+male
            if len(animals)>0 and self.goal in animals[0].habitat():
                result+=len(animals)
        return zone.total - result

class IntelligentAgent(ReactiveAgent):
    def __init__(self, sex: int):
        Agent.__init__(self, sex)
        self.feed_way='look_for_food'

    def habitat_heuristic(self, node):
        zone=node.state
        result=0
        for _, (female,male)  in zone.species.items():
            animals=female+male
            if len(animals)>0 and self.goal in animals[0].habitat():
                result+=len(animals)
        return zone.total - result

    def depredator_heuristic(self, node):
        zone=node.state
        result=0
        for _, (female,male)  in zone.species.items():
            animals=female+male
            if len(animals)>0 and self.goal in animals[0].habitat():
                result+=len(animals)
        return zone.total - result    
            

class BengalTiger(ReactiveAgent):
    _type = Specie.bengal_tiger

    def habitat(self): return [Habitat.polar, Habitat.tempered]
    def feed_on_vegetation(self): return False
    def life_expectancy(self): return (20,26)
    def speed(self): return(1,5)
    def prey(self): raise NotImplementedError()
    def depredator(self): raise NotImplementedError()
    def uninhabitable(self): raise NotImplementedError()
    def desnutrition(self): raise NotImplementedError()

class GrizzlyBear(ReactiveAgent):
    _type = Specie.grizzly_bear

    def habitat(self): return [Habitat.tropical, Habitat.desertic]
    def feed_on_vegetation(self): return False
    def life_expectancy(self): return (20,30)
    def speed(self): return(1,5)
    def prey(self): raise NotImplementedError()
    def depredator(self): raise NotImplementedError()
    def uninhabitable(self): raise NotImplementedError()
    def desnutrition(self): raise NotImplementedError()

class Horse(ReactiveAgent):
    _type = Specie.horse

    def habitat(self): return [Habitat.tropical, Habitat.desertic]
    def feed_on_vegetation(self): return True
    def life_expectancy(self): return (25,30)
    def speed(self): return(1,5)
    def prey(self): raise NotImplementedError()
    def depredator(self): raise NotImplementedError()
    def uninhabitable(self): raise NotImplementedError()
    def desnutrition(self): raise NotImplementedError()

class PolarBear(ReactiveAgent):
    _type = Specie.polar_bear

    def habitat(self): return [Habitat.polar, Habitat.tempered]
    def feed_on_vegetation(self): return True
    def life_expectancy(self): return (20,25)
    def speed(self): return(1,5)
    def prey(self): raise NotImplementedError()
    def depredator(self): raise NotImplementedError()
    def uninhabitable(self): raise NotImplementedError()
    def desnutrition(self): raise NotImplementedError()

class Rabbit(ReactiveAgent):
    _type = Specie.rabbit

    def habitat(self):return [Habitat.tropical, Habitat.desertic, Habitat.tempered, Habitat.polar]
    def feed_on_vegetation(self): return True
    def life_expectancy(self): return (7,9)
    def speed(self): return(1,5)
    def prey(self): raise NotImplementedError()
    def depredator(self): raise NotImplementedError()
    def uninhabitable(self): raise NotImplementedError()
    def desnutrition(self): raise NotImplementedError()

class Tiger(ReactiveAgent):
    _type = Specie.tiger

    def habitat(self): return [Habitat.tropical]
    def feed_on_vegetation(self): return False
    def life_expectancy(self): return (8,10)
    def speed(self): return(1,5)
    def prey(self): raise NotImplementedError()
    def depredator(self): raise NotImplementedError()
    def uninhabitable(self): raise NotImplementedError()
    def desnutrition(self): raise NotImplementedError()
      
class Ant(ReactiveAgent):
    _type = Specie.ant

    def habitat(): return [Habitat.desertic, Habitat.tropical]
    def feed_on_vegetation(): return True
    def life_expectancy(): return (1,2)
    def speed(): return(1,5)
    def prey(self): raise NotImplementedError()
    def depredator(self): raise NotImplementedError()
    def uninhabitable(self): raise NotImplementedError()
    def desnutrition(self): raise NotImplementedError()