import random
from .utils import Habitat
from .flock import Flock
type_temperature = {Habitat.Tropical:(17,26), Habitat.Desertic:(27,35), Habitat.Polar:(-5,10), Habitat.Tempered:(6,18)} 

class Zone:
    def __init__(self, zone_type):
        self.type = zone_type
        self.temperature_range = type_temperature[self.type]
        self.temperature = None
        self.flocks=[]

    def get_temperature(self):
        t_min,t_max = self.temperature_range
        return round(random.uniform(t_min, t_max),2)

    @property
    def total(self):
        total=0
        for flock in self.flocks:
            total+=flock.total
        return total

    def add_flock(self,flock):
        self.flocks.append(flock)

    def precipitations_event(self):
        self.temperature = self.get_temperature()
        # La probabilidad de que llueva mediante el evento Precipitaciones es uniforme y depende de la temperatura en la zona:
        #   Temperature          Probability
        #  (-inf, 10  ]              0
        #  (  10, 15  ]              0.03
        #  (  15, 17  ]              0.07
        #  (  17, 19  ]              0.11
        #  (  19, 21  ]              0.15
        #  (  21, 23  ]              0.37
        #  (  23, 25  ]              0.53
        #  (  25, 26  ]              0.17
        #  (  26, 28  ]              0.1
        #  (  28, 30  ]              0.05
        #  (  30, +inf)              0
        # 10ºC es la temperatura mínima y 30ºC es la temperatura máxima que se considera como posible para que llueva
        temp_prob = {(10,15):0.003,
                     (15,17):0.07,
                     (17,19):0.11,
                     (19,21):0.15,
                     (21,23):0.37,
                     (23,25):0.53,
                     (25,26):0.17,
                     (26,28):0.08,
                     (28,30):0.005}
        probability = random.uniform(0,1)
        for (t_min, t_max),prob in temp_prob.items():
            if t_min < self.temperature and self.temperature <= t_max:
                if probability > prob: return False
                return True
        else: return False