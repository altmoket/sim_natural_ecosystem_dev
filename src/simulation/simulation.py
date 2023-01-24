import random
from src.ecosystems import Ecosystem
import heapq as heap
from scipy.stats import expon, bernoulli
class Simulator:
    def __init__(self, ecosystem: Ecosystem, final_time: int):
        self.time = 0
        
        # Event times
        self.death_time = 0
        self.birth_time = 0
        self.heatwave_time = 0
        self.coldwave_time = 0
        
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
        self.birth_event()
        self.heatwave_event()
        self.coldwave_event()

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
            self.events_methods[event[1]]()

    def birth_event(self):
        self.time = self.birth_time
        self.birth_count += 1
        self.ecosystem.total_of_animals += 1
        output = self.ecosystem.max_probability()
        next_death_time = None
        if output: 
            specie, zone = output
            sex = self.generate_sex()
            zone.add_animal(specie(sex))
            print(f'Time: {int(self.time)}  Counter: {self.birth_count}  Event: Birth of a {specie._type} in {zone}')
            
            next_death_time = self.generate_death_time()
            self.death_time = self.time + next_death_time
            self.add_event(self.death_time, 'death')

        next_birth_time = self.generate_birth_time()
        self.birth_time = self.time+next_birth_time
        self.add_event(self.birth_time, 'birth')
        self.births_moments[self.birth_count] = self.time

        if next_death_time is None and self.ecosystem.total_of_animals > 100:
            next_death_time = self.generate_death_time()
            self.death_time = self.time + next_death_time
            self.add_event(self.death_time, 'death')

    def death_event(self):
        self.time = self.death_time
        self.death_count += 1
        self.ecosystem.total_of_animals = max(self.ecosystem.total_of_animals - 1, 0)
        if self.ecosystem.total_of_animals > 0:
            zone = random.choice(list(filter(lambda zone : zone.total > 0, self.ecosystem.zones)))
            specie = zone.remove_animmal()._type
            print(f'Time: {int(self.time)}  Counter: {self.death_count}  Event: Death of a {specie} in {zone}')
        
        self.deaths_moments[self.death_count] = self.time
        
    def heatwave_event(self):
        desertic_zones = self.ecosystem.desertic_zones
        if len(desertic_zones)>0:
            zone = random.choice(desertic_zones)
            self.time = self.heatwave_time
            self.heatwave_count += 1
            print(f"Time:{int(self.time)} Number: {self.heatwave_count}  Event: Heat Wave from {zone}")
            self.spread_heat(zone.adj_z) # Ordenar las zonas adjacentes por distancia. Agregar despues
            next_heatwave_time = self.generate_heatwave_time()
            self.heatwave_time = self.time + next_heatwave_time
            self.add_event(self.heatwave_time, 'heatwave')
            self.heatwave_moments[self.heatwave_count] = self.time
            
    def spread_heat(self, zones):
        for zone in zones: 
            response = zone.add_heatstroke()
            for action in response:
                if action['status'] == "GETTING HEAT STROKE":
                    print(f"Zone: {zone.id} has getting a heatstroke. Heatstroke Counter: {action['heatstrokes']}.")
                elif action['status'] == "MUTATING ZONE":
                    print(f"Zone: {zone.id} is mutating to {action['zone_type_destiny']} zone type from {action['zone_type']}")
                elif action['status'] == "ZONE TYPE HAS CHANGED":
                    print(f"Zone: {zone.id} has changed to {action['zone_type']}")
                else:
                    raise Exception("Unrecognized action")
                
    def coldwave_event(self):
        polar_zones = self.ecosystem.polar_zones
        if len(polar_zones)>0:
            zone = random.choice(polar_zones)
            self.time = self.coldwave_time
            self.coldwave_count += 1
            print(f"Time:{int(self.time)} Number: {self.coldwave_count}  Event: Cold Wave from {zone}")
            self.spread_cold(zone.adj_z) # Ordenar las zonas adjacentes por distancia. Agregar despues
            next_coldwave_time = self.generate_coldwave_time()
            self.coldwave_time = self.time + next_coldwave_time
            self.add_event(self.coldwave_time, 'coldwave')
            self.coldwave_moments[self.coldwave_count] = self.time
            
    def spread_cold(self, zones):
        for zone in zones: 
            response = zone.add_coldstroke()
            for action in response:
                if action['status'] == "GETTING COLD STROKE":
                    print(f"Zone: {zone.id} has getting a coldstroke. Coldstroke Counter: {action['coldstrokes']}.")
                elif action['status'] == "MUTATING ZONE":
                    print(f"Zone: {zone.id} is mutating to {action['zone_type_destiny']} zone type from {action['zone_type']}")
                elif action['status'] == "ZONE TYPE HAS CHANGED":
                    print(f"Zone: {zone.id} has changed to {action['zone_type']}")
                else:
                    raise Exception("Unrecognized action")
            
            
    def add_event(self, event_time, event):
        if event_time <= self.final_time:
            heap.heappush(self.events, (event_time, event))

    def generate_birth_time(self):
        return expon.rvs(1, size=1, scale=1)

    def generate_death_time(self):
        return expon.rvs(1, size=1, scale=1)
    
    def generate_heatwave_time(self):
        return expon.rvs(1, size=1, scale=1) # Modificar este parametro, no se cual distribucion poner
    
    def generate_coldwave_time(self):
        return expon.rvs(1, size=1, scale=1) # Modificar este parametro, no se cual distribucion poner

    def generate_sex(self):
        ber = bernoulli(p=0.5)
        return ber.rvs(1)[0]