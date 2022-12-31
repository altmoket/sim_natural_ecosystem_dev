import random
from .utils import Habitat
type_temperature = {Habitat.Tropical:(17,26), Habitat.Desertic:(27,35), Habitat.Polar:(-5,10), Habitat.Tempered:(6,18)} 

class Zone:
    def __init__(self, zone_type):
        self.type = zone_type
        self.temperature_range = type_temperature[self.type]
        self.temperature = None
        self.flocks:list[Flock]=[]

    def get_temperature(self):
        t_min,t_max = self.temperature_range
        return round(random.uniform(t_min, t_max),2)

    @property
    def total(self):
        total=0
        for flock in self.flocks:
            total+=flock.total
        return total

    def precipitations_event(self):
        self.temperature = self.get_temperature()
        temp_prob = {(10,15):0.003, (15,17):0.07, (17,19):0.11, (19,21):0.15, (21,23):0.37, (23,25):0.53, (25,26):0.17,
                     (26,28):0.08, (28,30):0.005}
        probability = random.uniform(0,1)
        for (t_min, t_max),prob in temp_prob.items():
            if t_min < self.temperature and self.temperature <= t_max:
                if probability > prob: return False
                return True
        else: return False

class Flock:
    def __init__(self, type:str, female_total:int=0, male_total:int=0):
        self.female_total = female_total
        self.male_total = male_total
        self.__type__ = type
        self.zone = None

    @property
    def total(self):
         return self.female_total + self.male_total

    def asign_zone(self, zone:Zone):
        self.zone = zone
        self.zone.flocks.append(self)

    def add_animal(self, sex:int):
        if sex == 0: self.male_total += 1
        else: self.female_total += 1

    def remove_animal(self, sex:int):
        if sex == 0: self.male_total -= 1
        else: self.female_total -= 1