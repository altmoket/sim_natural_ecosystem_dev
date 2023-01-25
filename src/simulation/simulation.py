import random
from src.ecosystems import Ecosystem
import heapq as heap
from scipy.stats import bernoulli
from ..components.utils import exponential 
from .printer import AnimalActionPrinter

printer = AnimalActionPrinter() # Aqui se le puede pasar un animal en concreto
                                # o dejarlo vacio, Pero para imprimir un mensaje
                                # tiene que estar seteado un animal,
                                # printer.animal = animal. 
class Simulator:
    def __init__(self, ecosystem: Ecosystem, final_day: int, final_year):
        self.day = 1
        self.year = 1
        
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
        self.final_day = final_day
        self.final_year = final_year
        
        # Init some events
        print(f"Year {self.year} of the Simulation")
        self.birth_event((self.year,self.day))
        self.death_event((self.year,self.day))
        self.heatwave_event((self.year,self.day))
        self.coldwave_event((self.year,self.day))

    @property
    def events_methods(self):
        events = {'birth': self.birth_event,
                  'death': self.death_event,
                  'heatwave': self.heatwave_event,
                  'coldwave': self.coldwave_event}
        return events

    def simulate(self):
        while len(self.events) > 0:
            event:tuple[int, int, function] = heap.heappop(self.events)
            year, day, item = event
            while (self.year < year or (self.year == year and self.day < day)):
                for zone in self.ecosystem.zones:
                    zone.get_weather(False)
                for zone in self.ecosystem.zones:
                    for _, (female, male) in zone.species.items():
                        for animal in female + male:
                            animal.get_action((self.day,zone,self.ecosystem.colony))
                    for animal in zone.limb:
                        animal.update((self.day,zone,self.ecosystem.colony))                
                print(f"Day: {self.day}  ACCIONES AGENTES")
                self.day += 1
                if self.day == 366: 
                    self.day = 1
                    self.year += 1
                    print(f"Year {self.year} of the Simulation")
            
            self.events_methods[item]((year,day))

        while (self.year < self.final_year or (self.year == self.final_year and self.day <= self.final_day)):
            for zone in self.ecosystem.zones:
                zone.get_weather(False)
            for zone in self.ecosystem.zones:
                for _, (female, male) in zone.species.items():
                    for animal in female + male:
                        animal.get_action((self.day,zone,self.ecosystem.colony))
                for animal in zone.limb:
                    animal.update((self.day,zone,self.ecosystem.colony))   
                print(f"Day: {self.day}  ACCIONES AGENTES")
                self.day += 1
                if self.day == 366: 
                    self.day = 1
                    self.year += 1
                    print(f"Year {self.year} of the Simulation")
                

    def birth_event(self, time):
        self.year, self.day = time
        output = self.ecosystem.max_probability()

        if output: 
            self.ecosystem.total_of_animals += 1
            specie, zone = output
            sex = self.generate_sex()
            zone.add_animal(specie(sex))
            self.birth_count += 1
            print(f'Day: {self.day}  Counter: {self.birth_count}  Event: Birth of a {specie.str()} in {zone}')
            self.births_moments[self.birth_count] = time

        next_birth_time = self.generate_birth_time(10)
        day = max(1, (next_birth_time + self.day) % 366)
        year = (next_birth_time + self.day) // 366 + self.year
        if year < self.final_year or (year == self.final_year and day <= self.final_day):
            heap.heappush(self.events, (year, day, 'birth'))

    def death_event(self, time):
        self.year, self.day = time
        total_of_animals = self.ecosystem.total_of_animals - 1

        if total_of_animals > 100:
            self.ecosystem.total_of_animals = total_of_animals
            zone = random.choice(list(filter(lambda zone : zone.total > 0, self.ecosystem.zones)))
            animal = zone.remove_animal()
            self.death_count += 1
            print(f'Day: {self.day}  Counter: {self.death_count}  Event: Death of a {type(animal).str()} in {zone}')
            self.deaths_moments[self.death_count] = time

        next_death_time = self.generate_death_time(15)
        day = max(1, (next_death_time + self.day) % 366)
        year = (next_death_time + self.day) // 366 + self.year
        if year < self.final_year or (year == self.final_year and day <= self.final_day):
            heap.heappush(self.events, (year, day, 'death'))    
        
    def heatwave_event(self, time):
        zone = random.choice(self.ecosystem.zones)
        zone.strokes += 1 if zone.strokes < 5 else zone.strokes
        self.year, self.day = time
        self.heatwave_count += 1
        print(f"Day: {self.day}  Counter: {self.heatwave_count}  Event: Heat Wave on {zone} ({zone.strokes})")
        if zone.strokes == 5:
            zone_type_destiny = zone.zone_type_destiny('heatstroke')
            if zone_type_destiny != zone.type:
                print(f"Zone: {zone.id} is mutating to {zone_type_destiny} zone type from {zone.type} zone type")
            zone.change_habitat(zone_type_destiny)

        next_heatwave_time = self.generate_heatwave_time(20)
        day = max(1, (next_heatwave_time + self.day) % 366)
        year = (next_heatwave_time + self.day) // 366 + self.year
        if year < self.final_year or (year == self.final_year and day <= self.final_day):
            heap.heappush(self.events, (year, day, 'heatwave'))

        self.heatwave_moments[self.heatwave_count] = time
                
    def coldwave_event(self, time):
        zone = random.choice(self.ecosystem.zones)
        zone.strokes -= 1 if zone.strokes > 0 else zone.strokes
        self.year, self.day = time
        self.coldwave_count += 1
        print(f"Day: {self.day}  Counter: {self.coldwave_count}  Event: Cold Wave on {zone} ({zone.strokes})")
        if zone.strokes == 0:
            zone_type_destiny = zone.zone_type_destiny('coldstroke')
            if zone_type_destiny != zone.type:
                print(f"Zone: {zone.id} is mutating to {zone_type_destiny} zone type from {zone.type} zone type")
            zone.change_habitat(zone_type_destiny)

        next_coldwave_time = self.generate_coldwave_time(20)
        day = max(1, (next_coldwave_time + self.day) % 366)
        year = (next_coldwave_time + self.day) // 366 + self.year
        if year < self.final_year or (year == self.final_year and day <= self.final_day):
            heap.heappush(self.events, (year, day, 'coldwave'))

        self.coldwave_moments[self.coldwave_count] = time                


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