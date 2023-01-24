import random
from .utils import Habitat, exponential
from ..components.species import Species
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
        self.species: defaultdict[Species, tuple[list[Species],list[Species]]] = defaultdict(lambda : ([],[]))
        self.adj_z:dict[Zone,int] = {}  
        self.limb:list[tuple[Species, int, int]] = []
        self.total=0
        self.get_weather()
        self.max_heatstrokes = 15
        self.heatstrokes = 0
        self.max_coldstrokes = 15
        self.coldstrokes = 0

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

    def add_animal(self, animal:Species):
        specie, sex = animal._type, animal.sex
        self.species[specie][sex].append(animal)
        self.total+=1

    def remove_animmal(self):
        no_empty=lambda specie : (len(self.species[specie][0])+len(self.species[specie][1]))>0
        specie = random.choice(list(filter(no_empty,list(self.species.keys()))))
        list_sex = random.choice(list(filter(lambda animal_list:len(animal_list)>0,self.species[specie])))
        animal=random.choice(list_sex)
        list_sex.remove(animal)
        self.total-=1
        return animal 
        
    def create_animal(self, animal:Species):
        animal.birthday = random.randint(2,365)
        t_min = animal.life_expectancy()[0]
        animal.age = random.randint(0,t_min-1)
        self.add_animal(animal)

    def delete_animmal(self, animal:Species):
        self.species[animal._type][animal.sex].remove(animal)
        self.total-=1

    def actions_generator(self, time):
        for _,(female, male) in self.species.items():
            for animal in female: animal.reaction((time, self))
            for animal in male: animal.reaction((time, self))
        for i, (animal,time_local) in enumerate(self.limb):
            if time_local==time:
                death = animal.update(time,self)
                if death: self.limb.remove(animal)
                elif animal.time_limb == 0: 
                    self.limb.pop(i)
                    self.add_animal(animal)

    def animals_in_own_habitat(self):
        output=list(self.species.keys())
        output=list(filter(lambda specie: self.type in Species.search(specie).habitat() ,output))
        return output
        
    def add_heatstroke(self):
        self.heatstrokes += 1 if self.type != Habitat.desertic else 0
        response = []
        response.append({"status": "GETTING HEAT STROKE", "heatstrokes": self.heatstrokes})
        if self.heatstrokes == self.max_heatstrokes:
            zone_type_destiny = self.zone_type_destiny('heatstroke')
            zone_type_destiny_str = str(zone_type_destiny).upper()
            response.append({ 'status': "MUTATING ZONE", "zone_type_destiny": zone_type_destiny_str, 'zone_type': self.zone_type})
            self.change_habitat(zone_type_destiny)
            response.append({'status': "ZONE TYPE HAS CHANGED", "zone_type": self.zone_type})
        return response
    
    def add_coldstroke(self):
        self.coldstrokes += 1 if self.type != Habitat.polar else 0
        response = []
        response.append({"status": "GETTING COLD STROKE", "coldstrokes": self.coldstrokes})
        if self.coldstrokes == self.max_coldstrokes:
            zone_type_destiny = self.zone_type_destiny('coldstroke')
            zone_type_destiny_str = str(zone_type_destiny).upper()
            response.append({ 'status': "MUTATING ZONE", "zone_type_destiny": zone_type_destiny_str, 'zone_type': self.zone_type})
            self.change_habitat(zone_type_destiny)
            response.append({'status': "ZONE TYPE HAS CHANGED", "zone_type": self.zone_type})
        return response
        
    def change_habitat(self, habitat):
        self.type = habitat
        self.weather = None             
        self.floor = 0  
        v_min, v_max = type_zone[self.type]['vegetation']         
        self.vegetation = round(random.uniform(v_min, v_max), 3)
        self.get_weather()
        self.max_heatstrokes = 15
        self.heatstrokes = 0
        self.max_coldstrokes = 15
        self.coldstrokes = 0
    
    def zone_type_destiny(self, param):
        index = zone_mutation.index(self.type)
        if param == 'heatstroke':
            return zone_mutation[index + 1]
        elif param == 'coldstroke':
            return zone_mutation[index - 1]
    
    @property
    def zone_type(self):
        return str(self.type).upper()
        
    def __str__(self) -> str:
        return f'Zone {self.id}: {self.type}'

    def __repr__(self) -> str:
        return f'Zone {self.id}: {self.type}'