from src.ecosystems import Ecosystem
import heapq as heap
from scipy.stats import expon, bernoulli
import random

class Simulator:
    def __init__(self,ecosystem:Ecosystem,final_time:int):      
        self.time = 0
        self.death_time = 0
        self.birth_time = 0
        self.precipitation_time = 0
        self.birth_count = 0
        self.death_count = 0
        self.precipitation_count = 0
        self.births_moments = {}
        self.deaths_moments = {} 
        self.ecosystem=ecosystem
        self.events=[]
        self.final_time=final_time
        self.birth_event()
        self.precipitations_event()

    @property
    def events_methods(self):
        events={'birth':self.birth_event,
                'death':self.death_event,
                'precipitation':self.precipitations_event
                }
        return events

    def simulate(self):
        while len(self.events)>0:
            event:tuple(int,function)=heap.heappop(self.events)
            self.events_methods[event[1]]()

    def birth_event(self):
        self.time = self.birth_time
        self.birth_count +=1
        self.ecosystem.total_of_animals+=1
        flock = self.ecosystem.max_probability(True)
        sex = self.generate_sex()
        flock.add_animal(sex)
        print(f'Time:{int(self.time)}  Number: {self.birth_count}  Event: Birth of a {flock.__type__}')
        if self.birth_count < 20 :
            next_birth_time = self.generate_birth_time()
            self.birth_time = self.time+next_birth_time
            if self.birth_time < self.final_time: heap.heappush(self.events,(self.birth_time,'birth'))
        self.births_moments[self.birth_count] = self.time
        if self.birth_count == 1:
            next_death_time = self.generate_death_time()
            self.death_time = self.time + next_death_time
            heap.heappush(self.events,(self.death_time,'death'))

    def death_event(self):
        self.time = self.death_time
        self.death_count +=1
        self.ecosystem.total_of_animals-=1
        flock = self.ecosystem.max_probability(False)
        sex=self.generate_sex()
        flock.remove_animal(sex)
        print(f'Time:{int(self.time)}  Number: {self.death_count}  Event: Death of a {flock.__type__}')
        if self.ecosystem.total_of_animals > 0:
            next_death_time = self.generate_death_time()
            self.death_time = self.time + next_death_time
            if self.death_time < self.final_time: heap.heappush(self.events,(self.death_time,'death'))
        self.deaths_moments[self.death_count] = self.time

    def precipitations_event(self):
        self.time = self.precipitation_time
        zone = random.choice(self.ecosystem.zones)
        temperature = zone.get_temperature()
        temp_prob = {(10,15):0.003, (15,17):0.07, (17,19):0.11, (19,21):0.15, (21,23):0.37, (23,25):0.53, (25,26):0.17,
                     (26,28):0.08,  (28,30):0.005}
        probability = random.uniform(0,1)
        for (t_min, t_max),prob in temp_prob.items():
            if t_min < temperature and temperature <= t_max:
                if probability <= prob:
                    print(f'Time:{int(self.time)}  Zone{zone.id}: {zone.type} is raining')
        self.precipitation_time = self.time + expon.rvs(1,size=1,scale=1)
        if self.precipitation_time < self.final_time:
            heap.heappush(self.events,(self.precipitation_time,'precipitation'))

    def generate_birth_time(self):
        return expon.rvs(1,size=1,scale=1)
    def generate_death_time(self):
        return expon.rvs(1,size=1,scale=1) 
    def generate_sex(self):
        ber=bernoulli(p=0.5)
        return ber.rvs(1)