from ..components import Zone, Specie,Species
from src.components.utils.tools import Habitat
from ..algorithms import CSP
import random
class Ecosystem:
    def __init__(self, zones: list[Zone], animals: list[Species] = None, adj_z: dict[Zone, list[Zone]] = None, adj_e: dict[Specie, list[Specie]] = None):
        self.zones = zones
        self.__set_distribution(animals, zones, adj_z, adj_e)
        self.total_of_animals = 0
        for zone in self.zones:
            self.total_of_animals += zone.total

    def __set_distribution(self, animals: list[Species], zones: list[Zone], adj_z: dict[Zone, list[Zone]], adj_e: dict[Specie, list[Specie]]):
        if animals and adj_e and adj_z:
            distribution = CSP(animals, zones, adj_z, adj_e)
            for item in distribution.items():
                item[1].add_animal(item[0])
                
    @property
    def desertic_zones(self):
        return [zone for zone in self.zones if zone.type == Habitat.desertic]
    
    @property
    def polar_zones(self):
        return [zone for zone in self.zones if zone.type == Habitat.polar]

    def max_probability(self):
        max =0
        output=None
        for zone in self.zones:
                for specie,(female,male) in zone.species.items():
                    peers=min(len(female),len(male))
                    if peers>0:
                        own_habitat= 2 if zone.type in female[0].habitat() else 1 
                        current=peers*own_habitat
                        if current >= max  :
                            max=current
                            output=(specie,zone)
        if output == None:
            zone=random.choice(self.zones)
            specie=random.choice(list(zone.species.keys()))
        output=(Species.search_specie_type(specie),zone)
        return output
    