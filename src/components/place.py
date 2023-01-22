import random
from .utils import Habitat,heap, exponential
from ..components.species import Species
type_zone = {Habitat.tropical:{'temperature':(17, 26),'vegetation':(90, 100)}, 
            Habitat.desertic: {'temperature':(27, 35),'vegetation':(25,  35)},
            Habitat.polar:    {'temperature':(-5, 10),'vegetation':(65,  80)}, 
            Habitat.tempered: {'temperature':( 6, 18),'vegetation':(75,  85)}}

class Zone:
    def __init__(self, _id: int, _type):
        self.id = _id
        # Conjunto de Percepciones del Entorno
        self.type = _type             
        self.weather = None             
        self.floor = 0  
        v_min, v_max = type_zone[self.type]['vegetation']         
        self.vegetation = round(random.uniform(v_min, v_max), 3)        
        self.flocks: list[Flock] = []
        self.adj_z:list[Zone] = []  
        self.distance_adj_z: dict[Zone,int] = {}
        self.get_weather()

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


    def add_flock(self, flock):
        self.flocks.append(flock)
        
    def __str__(self) -> str:
        return f'Zone {self.id}: {self.type}'

    def __repr__(self) -> str:
        return f'Zone {self.id}: {self.type}'

    @property
    def total(self):
        total = 0
        for flock in self.flocks:
            total += flock.total
        return total


class Flock:
    def __init__(self, type: str, female_total: int = 0, male_total: int = 0):
        self.__type__ = type
        self.health = round(random.uniform(92,100),3)
        specie = Species.search_specie_type(self.__type__)
        l_min, l_max = specie.life_expectancy()
        self.life_expectancy = random.randint(l_min,l_max)
        self.female_total = female_total
        self.male_total = male_total
        self.zone = None
        self.time_age_count:dict[int,list[tuple[int,int,int]]] = {}
        self.asign_animal(self.female_total,self.male_total)
        self.history = []

    @property
    def total(self):
        return self.female_total + self.male_total

    def asign_zone(self, zone: Zone):
        zone.add_flock(self)
        self.zone = zone

    def add_animal(self, day, sex: int):
        self.male_total += (1 - sex)
        self.female_total += sex
        self.mod_property(day, 0, sex, (1-sex))

    def remove_animal(self, sex:int):
        day = random.choice(list(self.time_age_count.keys()))
        list_heap = self.time_age_count[day]
        a,f,m = random.choice(list_heap)
        if f > 0 and m > 0:
            if sex == 0:
                self.male_total -= 1
                self.mod_property(day, a, f, -1)
            else:
                self.female_total -= 1
                self.mod_property(day, a, -1, m)
        elif f > 0 and sex == 1:
            self.female_total -= 1
            self.mod_property(day, a, -1, m)
        elif m > 0 and sex == 0:
            self.male_total -= 1
            self.mod_property(day, a, f, -1)
        else:
            if f > 0: 
                self.female_total -= 1
                self.mod_property(day, a, -1, m)
            else: 
                self.male_total -= 1
                self.mod_property(day, a, f, -1)

    def asign_animal(self, female_count, male_count):
        specie = Species.search_specie_type(self.__type__)
        t_min = specie.life_expectancy()[0]
        for i in range(female_count+male_count):
            day = random.randint(2, 365)
            age = random.randint(0, t_min-1)
            if i < female_count: self.mod_property(day, age, 1, 0)
            else: self.mod_property(day, age, 0, 1)

    def mod_property(self, day:int, age:int, female_count:int, male_count:int):
        try:
            list_heap = self.time_age_count[day]
            for index,(a,f,m) in enumerate(list_heap):
                if a == age:
                    if f+female_count == 0 and m+male_count == 0: list_heap.pop(index)
                    else:
                        list_heap[index] = (a,f+female_count,m+male_count)
                    if len(list_heap) == 0: self.time_age_count.pop(day,None)
                    if len(self.time_age_count) == 0: del self
                    return
            heap.push(list_heap,(age,female_count,male_count))
        except:
            list_heap = []
            heap.push(list_heap,(age,female_count,male_count))
            self.time_age_count[day] = list_heap

    def state_choice(self):
        zone = self.zone
        pass