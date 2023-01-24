import random
from src.ecosystems import Ecosystem
import heapq as heap
from scipy.stats import bernoulli
from ..components.utils import exponential 
class Simulator:
    def __init__(self, ecosystem: Ecosystem, final_time: int):
        self.time = 1
        self.age = 1
        
        # Event counters
        self.birth_count = 0
        self.death_count = 0
        self.heatwave_count = 0
        self.coldwave_count = 0
        
        # Event history
        self.births_moments = {}
        self.deaths_moments = {}
        self.heatwave_moments = {}
        self.coldwave_moments = {}
        
        self.ecosystem = ecosystem
        self.events = []
        self.final_time = final_time
        
        # Init some events
        print(f"Year {self.age} of the Simulation")
        self.birth_event(self.time)
        self.heatwave_event(self.time)
        self.coldwave_event(self.time)

    @property
    def events_methods(self):
        events = {'birth': self.birth_event,
                  'death': self.death_event,
                  'heatwave': self.heatwave_event,
                  'coldwave': self.coldwave_event}
        return events

    def simulate(self):
        while len(self.events) > 0:
            event: tuple(int, function) = heap.heappop(self.events)
            self.events_methods[event[1]](event[0])
            #self.time += 1
            #if self.time == 366: 
            #   self.time = 1
            #   self.age += 1
            # print(f"Year {self.age} of the Simulation")

    def birth_event(self, time):
        self.time = time
        self.birth_count += 1
        self.ecosystem.total_of_animals += 1
        output = self.ecosystem.max_probability()
        next_death_time = None
        if output: 
            specie, zone = output
            sex = self.generate_sex()
            zone.add_animal(specie(sex))
            print(f'Time: {self.time}  Counter: {self.birth_count}  Event: Birth of a {specie._type} in {zone}')
            
            next_death_time = self.generate_death_time(12)
            next_death_time += self.time
            if next_death_time <= self.final_time:
                heap.heappush(self.events, (next_death_time, 'death'))

        next_birth_time = self.generate_birth_time(10)
        next_birth_time += self.time
        if next_birth_time <= self.final_time:
                heap.heappush(self.events, (next_birth_time, 'birth'))

        self.births_moments[self.birth_count] = self.time
        if next_death_time is None and self.ecosystem.total_of_animals > 100:
            next_death_time = self.generate_death_time(15)
            next_death_time += self.time
            if next_death_time <= self.final_time:
                heap.heappush(self.events, (next_death_time, 'death'))

    def death_event(self, time):
        self.time = time
        self.death_count += 1
        self.ecosystem.total_of_animals = max(self.ecosystem.total_of_animals - 1, 0)
        if self.ecosystem.total_of_animals > 0:
            zone = random.choice(list(filter(lambda zone : zone.total > 0, self.ecosystem.zones)))
            specie = zone.remove_animmal()._type
            print(f'Time: {self.time}  Counter: {self.death_count}  Event: Death of a {specie} in {zone}')
        
        self.deaths_moments[self.death_count] = self.time
        
    def heatwave_event(self, time):
        zone = random.choice(self.ecosystem.zones)
        zone.strokes += 1 if zone.strokes < 5 else zone.strokes
        self.time = time
        self.heatwave_count += 1
        print(f"Time: {self.time}  Counter: {self.heatwave_count}  Event: Heat Wave on {zone} ({zone.strokes})")
        if zone.strokes == 5:
            zone_type_destiny = zone.zone_type_destiny('heatstroke')
            if zone_type_destiny != zone.type:
                print(f"Zone: {zone.id} is mutating to {zone_type_destiny} zone type from {zone.type} zone type")
                zone.change_habitat(zone_type_destiny)

        next_heatwave_time = self.generate_heatwave_time(20)
        next_heatwave_time += self.time
        if next_heatwave_time <= self.final_time:
                heap.heappush(self.events, (next_heatwave_time, 'heatwave'))

        self.heatwave_moments[self.heatwave_count] = self.time
                
    def coldwave_event(self, time):
        zone = random.choice(self.ecosystem.zones)
        zone.strokes -= 1 if zone.strokes > 0 else zone.strokes
        self.time = time
        self.coldwave_count += 1
        print(f"Time: {self.time}  Counter: {self.coldwave_count}  Event: Cold Wave on {zone} ({zone.strokes})")
        if zone.strokes == 0:
            zone_type_destiny = zone.zone_type_destiny('coldstroke')
            if zone_type_destiny != zone.type:
                print(f"Zone: {zone.id} is mutating to {zone_type_destiny} zone type from {zone.type} zone type")
                zone.change_habitat(zone_type_destiny)

        next_coldwave_time = self.generate_coldwave_time(20)
        next_coldwave_time += self.time
        if next_coldwave_time <= self.final_time:
                heap.heappush(self.events, (next_coldwave_time, 'coldwave'))

        self.coldwave_moments[self.coldwave_count] = self.time                


    def generate_birth_time(self, lbd):
        return int(exponential(1/lbd))

    def generate_death_time(self, lbd):
        return int(exponential(1/lbd))
    
    def generate_heatwave_time(self, lbd):
        return int(exponential(1/lbd))
    
    def generate_coldwave_time(self, lbd):
        return int(exponential(1/lbd))

    def generate_sex(self):
        ber = bernoulli(p=0.5)
        return int(ber.rvs(1)[0])