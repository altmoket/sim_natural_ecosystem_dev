from ..components import Zone, Specie,Species
from src.components.utils.tools import Habitat
from ..algorithms import AntColony, CSP
import random
class Ecosystem:
    def __init__(self, zones: list[Zone], animals: list[Species] = None, adj_z: dict[Zone, list[Zone]] = None, adj_e: dict[Specie, list[Specie]] = None):
        self.zones = zones
        self.__set_distribution(animals, zones, adj_z, adj_e)
        self.total_of_animals = 0
        for zone in self.zones:
            self.total_of_animals += zone.total
        self.colony=AntColony(decay=1, alpha=1, beta=0.5, delta_tau = 0.2 )

    def __set_distribution(self, animals: list[Species], zones: list[Zone], adj_z: dict[Zone, list[Zone]], adj_e: dict[Specie, list[Specie]]):
        if animals and adj_e and adj_z:
            distribution = CSP(animals, zones, adj_z, adj_e)
            for item in distribution.items():
                item[1].create_animal(item[0])
                
    @property
    def desertic_zones(self):
        return [zone for zone in self.zones if zone.type == Habitat.desertic]
    
    @property
    def polar_zones(self):
        return [zone for zone in self.zones if zone.type == Habitat.polar]

    def max_probability(self):
        balance = math.inf
        output = None
        specie_type = None
        for zone in self.zones:
            for specie,(female,male) in zone.species.items():
                peers = min(len(female),len(male))
                if peers > 0:
                    own_habitat = 2 if zone.type in female[0].habitat() else 1 
                    peers = len(female) + len(male)
                    current = peers * own_habitat
                    if current < balance:
                        balance = current
                        specie_type = self.give_cls_type(specie, Species) if specie != 'base' else None
                        if specie_type: output = (specie_type, zone)
                        else: raise Exception(f'Impossible to create animal with type: {specie}')
        return output

    def give_cls_type(self, _type, cls):
        for sbcls in cls.__subclasses__():
            if sbcls._type == _type: return sbcls
            result = self.give_cls_type(_type, sbcls)
            if result: return result
        return None

    