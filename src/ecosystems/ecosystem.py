from ..components import Zone, Species
from ..algorithms import CSP, AntColony
import math

class Ecosystem:
    def __init__(self, zones:list[Zone], animals:list[Species]=None):
        self.zones = zones
        self.__set_distribution(animals, zones)
        self.colony=AntColony(decay=1, alpha=1, beta=0.5, delta_tau = 0.2 )

    @property
    def total_of_animals(self):
        total = 0
        for zone in self.zones:
            total += zone.total + len(zone.limb)
        return total

    def __set_distribution(self, animals:list[Species], zones:list[Zone]):
        adj_z = {key:list(key.adj_z.keys()) for key in zones}
        adj_e = {type(key):type(key).prey() for key in animals}
        if animals and adj_e and adj_z:
            distribution = CSP(animals, zones, adj_z, adj_e)
            for item in distribution.items():
                item[1].create_animal(item[0])

    def max_probability(self):
        balance = math.inf
        output = None
        specie_type = None
        for zone in self.zones:
            for specie,(female,male) in zone.species.items():
                peers = min(len(female),len(male))
                if peers > 0:
                    own_habitat = 2 if zone.type in specie.habitat() else 1 
                    peers = len(female) + len(male)
                    current = peers * own_habitat
                    if current < balance:
                        balance = current
                        output = (specie, zone)
        return output

    