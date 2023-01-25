import random
from .utils import Habitat, exponential
from collections import defaultdict

type_zone = {Habitat.tropical:{'temperature':(17, 26),'vegetation':(90, 100)}, 
            Habitat.desertic: {'temperature':(27, 35),'vegetation':(25,  35)},
            Habitat.polar:    {'temperature':(-5, 10),'vegetation':(65,  80)}, 
            Habitat.tempered: {'temperature':( 6, 18),'vegetation':(75,  85)}}
zone_mutation = [Habitat.polar, Habitat.tempered, Habitat.tropical, Habitat.desertic]

class Zone:
    def __init__(self, _id: int, _type:Habitat):
        self.id = _id
        # Conjunto de Percepciones del Entorno
        self.type = _type             
        self.weather = None             
        self.floor = 0  
        v_min, v_max = type_zone[self.type]['vegetation']         
        self.vegetation = round(random.uniform(v_min, v_max), 3)        
        self.species = defaultdict(lambda : ([],[]))
        self.adj_z= {}  
        self.limb = []
        self.total=0
        self.get_weather()
        self.strokes = 3

    # De invocar este metodo solo se encarga la Simulacion
    def get_weather(self):
        t_min, t_max = type_zone[self.type]['temperature']
        temperature = round(random.uniform(t_min, t_max), 2)
        temp_prob = {(10, 15): 0.003, (15, 17): 0.07, (17, 19): 0.11, (19, 21): 0.15, (21, 23): 0.37, (23, 25): 0.45, (25, 26): 0.17,
                     (26, 28): 0.08,  (28, 30): 0.005}
        probability = random.uniform(0, 1)
        for (t_min, t_max), prob in temp_prob.items():
            if t_min < temperature and temperature <= t_max:
                if probability <= prob:
                    self.weather = temperature, True
                    self.vegetation = self.vegetation + 0.3 if self.vegetation + 0.3 <= 100 else 100
                    self.floor = self.floor + 1 + int(exponential(1.5))
                    print(f'{str(self)} with temperature {temperature}, is raining')
                else:
                    self.weather = temperature, False
                    self.floor = self.floor - 1 if self.floor > 0 else 0
                    print(f'{str(self)} with temperature {temperature}, is not raining')
                break
        else:
            self.weather = temperature, False
            self.floor = self.floor - 1 if self.floor > 0 else 0
            print(f'{str(self)} with temperature {temperature}, is not raining')

    def add_animal(self, animal):
        specie, sex = animal._type, animal.sex
        self.species[specie][sex].append(animal)
        self.total+=1

    def remove_animal(self):
        no_empty = lambda specie : (len(self.species[specie][0])+len(self.species[specie][1]))>0
        specie = random.choice(list(filter(no_empty,list(self.species.keys()))))
        list_sex = random.choice(list(filter(lambda animal_list:len(animal_list)>0,self.species[specie])))
        animal=random.choice(list_sex)
        list_sex.remove(animal)
        self.total-=1
        return animal 
        
    def create_animal(self, animal):
        animal.birthday = random.randint(2,365)
        t_min = animal.life_expectancy()[0]
        animal.age = random.randint(0,t_min-1)
        self.add_animal(animal)

    def delete_animal(self, animal):
        self.species[animal._type][animal.sex].remove(animal)
        self.total-=1

    def actions_generator(self, time,colony):
        for _,(female, male) in self.species.items():
            for animal in female: animal.reaction((time, self,colony))
            for animal in male: animal.reaction((time, self,colony))
        for i, (animal,time_local) in enumerate(self.limb):
            if time_local==time:
                death = animal.update(time,self)
                if death: self.limb.remove(animal)
                elif animal.time_limb == 0: 
                    self.limb.pop(i)
                    self.add_animal(animal)
        
    def change_habitat(self, habitat):
        self.type = habitat             
        self.floor = 0  
        v_min, v_max = type_zone[self.type]['vegetation']         
        self.vegetation = round(random.uniform(v_min, v_max), 3)
        t_min, t_max = type_zone[self.type]['temperature']
        temperature = round(random.uniform(t_min, t_max), 2)
        self.weather = (temperature, False)
        self.strokes = 3
    
    def zone_type_destiny(self, param):
        index = zone_mutation.index(self.type)
        if param == 'heatstroke':
            index = min(index + 1, len(zone_mutation) - 1)
            return zone_mutation[index]
        elif param == 'coldstroke':
            index = max(index - 1, 0)
            return zone_mutation[index]
        
    def __str__(self) -> str:
        return f'Zone {self.id}: {self.type}'

    def __repr__(self) -> str:
        return f'Zone {self.id}: {self.type}'