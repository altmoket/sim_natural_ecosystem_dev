from .utils import Habitat,Specie
import random
#from ..algorithms import astar

class Species:
    _type = Specie.base
    @classmethod
    def search_specie_type(self, name: property):
        for cls in self.__subclasses__():
            if cls._type == name:
                return cls
        raise Exception("Unknown Specie")
    def __init__(self,sex:int):
        self.birthday=0
        self.age=0
        self.sex=sex
        self.health = round(random.uniform(92,100),3)
        self.full = round(random.uniform(92,100),3)
        self.time_death = random.randint(self.life_expectancy()[0], self.life_expectancy()[1])
        self.my_speed = random.randint(self.speed()[0], self.speed()[1])
    @classmethod
    def habitat(self): raise NotImplementedError()
    @classmethod
    def feed_on_vegetation(self): raise NotImplementedError()
    @classmethod
    def life_expectancy(self): raise NotImplementedError()
    @classmethod
    def speed(self): raise NotImplementedError()
    @classmethod
    def attack_power(self): raise NotImplementedError()
    @classmethod
    def defense_power(self): raise NotImplementedError()
    @classmethod
    def prey(self): raise NotImplementedError()
    @classmethod
    def depredator(self): raise NotImplementedError()
    @classmethod
    def uninhabitable(self): raise NotImplementedError()
    @classmethod
    def desnutrition(self): raise NotImplementedError()

    #BORRAAAAAAAAR
    def reaction(self, state):pass
    def get_action(self, state):pass
    def death(self, state):pass
    def feed_weight(self, state):pass
    def migrate_weight(self, state):pass 

class ReactiveAgent(Species):
    _type = "reactive"
    def __init__(self, sex:int):
        Species.__init__(self,sex)
        self.path = []
        self.next_zone = None
        self.ate=False
        self.time_limb = 0
        self.is_starving=False

    def update(self,state):
        time, zone = state
        hungry = 0 if self.ate else self.desnutrition()
        self.full=max(0,self.full- hungry)
        self.health = max(0, self.health - hungry - self.uninhabitable()[zone.type])
        if self.health == 0: return True
        if self.time_limb > 0:
            if time == self.birthday: self.age += 1
            if self.age == self.time_death: return True
            floor = 1 if zone.floor > 0 else 0
            self.time_limb = self.time_limb -1 + floor
        self.ate=False

    def reaction(self, state):
        time, zone = state
        if time == self.birthday: self.age += 1
        action = self.get_action(state)
        if action == 'death':
            zone.delete_animal(self)
        elif action == 'migrate':
            self.path[0].delete_animal(self)
            if 1- self.full/100 > 0.7: self.feed_here(self.path[0])
            self.path.pop(0)
            distance:int = zone.adj_z[self.path[0]]
            self.time_limb = max(1,distance // self.my_speed)
            if len(self.path)>0 : self.path[0].limb.append((self, time))
        elif action == 'feed':
            self.feed_here(zone)
            if not self.ate:
                if not self.is_starving:
                    self.is_starving=True
                    next_zone , trip_time =self.get_next_zone(zone)
                    self.time_limb=trip_time
                    next_zone.limb.append((self,time))
                else: self.is_starving=False     
        self.update(state)

    def get_action(self, state):
        time, zone = state
        if time == self.time_death: return 'death'
        if self.is_starving: return 'feed'
        if len(self.path)>0 : return 'migrate'
        weight1= self.feed(state)
        path, weight2= self.migrate(state)
        if weight2 < 0.3 and  weight1 < 0.3: return 'nothing'
        if weight2 > weight1 :
            self.path=path
            return 'migrate'
        return 'feed'


    def get_next_zone(self,zone):
        max = 0
        result=None
        time=0
        for next_zone,distance in zone.adj_z.items():
            current =  next_zone.vegetation  if self.feed_on_vegetation() > 0 else 0 # vegetaciondde la zona
            for animal in self.prey:
                current+= len(zone.species[animal][0])+len(zone.species[animal][1]) #cantida de presas en la zona
            trip_time=max(1,distance//self.my_speed)
            current-= self.uninhabitable()[next_zone] * (trip_time) # nivel de salud que resta cruzar hacia la zona 
            for animal in self.depredator:
                current-= len(zone.species[animal][0])+len(zone.species[animal][1]) # cantidad de depredadores en la zona
            if result==None: 
                max=current
                result=next_zone
                time=trip_time
            else:
                if current>max:
                    max=current
                    result=next_zone
                    time=trip_time
            return result, time

    def feed_here(self,zone):
            if self.feed_on_vegetation()>0 and zone.vegetation >0:
                zone.vegetation =max(0,zone.vegetation- self.feed_on_vegetation())
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
 
    def feed_weight(self, state):
        result= self.full/100

    def migrate_weight(self, state):
        _,zone=state
        weight=0
        path=None
        if not zone.type in self.habitat:
            path=astar(zone)
            if len(path)>0:
                current_weight=self.get_weight(path)
                if current_weight>0:
                    weight=current_weight
        depredators=list(filter(lambda specie : specie in self.prey(),zone.species.keys()))
        if len(depredators)>0:
            currentpath=astar(zone)
            if len(currentpath)>0:
                current_weight=self.get_weight(path)
                if current_weight>0 and current_weight<=weight:
                    path = currentpath
        return path,weight

    def get_weight(self,path):
        health_left=self.health
        current_zone=path[0]
        for next_zone in path[1:]:
            distance:int = current_zone.adj_z[next_zone]
            time_limb = max(1,distance // self.my_speed)
            health_left=max(0,health_left-time_limb * self.desnutrition())
        return health_left/100
        
class IntelligentAgent(ReactiveAgent):
    _type = "intelligent"

    def get_next_zone(self,zone):
        pass

class BengalTiger(Species):
    _type = Specie.bengal_tiger
    @classmethod
    def habitat(self): return [Habitat.polar, Habitat.tempered]
    @classmethod
    def feed_on_vegetation(self): return False
    @classmethod
    def life_expectancy(self): return (20,26)
    @classmethod
    def speed(self): return(1,5)
    @classmethod
    def attack_power(self): pass
    @classmethod
    def defense_power(self): pass


class GrizzlyBear(Species):
    _type = Specie.grizzly_bear
    @classmethod
    def habitat(self): return [Habitat.tropical, Habitat.desertic]
    @classmethod
    def feed_on_vegetation(self): return False
    @classmethod
    def life_expectancy(self): return (20,30)
    @classmethod
    def speed(self): return(1,5)
    @classmethod
    def attack_power(self): pass
    @classmethod
    def defense_power(self): pass


class Horse(Species):
    _type = Specie.horse
    @classmethod
    def habitat(self): return [Habitat.tropical, Habitat.desertic]
    @classmethod
    def feed_on_vegetation(self): return True
    @classmethod
    def life_expectancy(self): return (25,30)
    @classmethod
    def speed(self): return(1,5)
    @classmethod
    def attack_power(self): pass
    @classmethod
    def defense_power(self): pass


class PolarBear(Species):
    _type = Specie.polar_bear
    @classmethod
    def habitat(self): return [Habitat.polar, Habitat.tempered]
    @classmethod
    def feed_on_vegetation(self): return True
    @classmethod
    def life_expectancy(self): return (20,25)
    @classmethod
    def speed(self): return(1,5)
    @classmethod
    def attack_power(self): pass
    @classmethod
    def defense_power(self): pass


class Rabbit(Species):
    _type = Specie.rabbit
    @classmethod
    def habitat(self):return [Habitat.tropical, Habitat.desertic, Habitat.tempered, Habitat.polar]
    @classmethod
    def feed_on_vegetation(self): return True
    @classmethod
    def life_expectancy(self): return (7,9)
    @classmethod
    def speed(self): return(1,5)
    @classmethod
    def attack_power(self): pass
    @classmethod
    def defense_power(self): pass

class Tiger(Species):
    _type = Specie.tiger
    @classmethod
    def habitat(self): return [Habitat.tropical]
    @classmethod
    def feed_on_vegetation(self): return False
    @classmethod
    def life_expectancy(self): return (8,10)
    @classmethod
    def speed(self): return(1,5)
    @classmethod
    def attack_power(self): pass
    @classmethod
    def defense_power(self): pass
      
class Ant(Species):
    _type = Specie.ant
    def habitat(): return [Habitat.desertic, Habitat.tropical]
    def feed_on_vegetation(): return True
    def life_expectancy(): return (1,2)
    def speed(): return(1,5)
    def attack_power(): pass
    def defense_power(): pass