from ..components import Zone, Flock, Specie
from ..algorithms import CSP

class Ecosystem:
    def __init__(self, zones: list[Zone], flocks: list[Flock] = None, adj_z: dict[Zone, list[Zone]] = None, adj_e: dict[Specie, list[Specie]] = None):
        self.zones = zones
        self.__set_distribution(flocks, zones, adj_z, adj_e)
        self.total_of_animals = 0
        for zone in self.zones:
            self.total_of_animals += zone.total

    def __set_distribution(self, flocks: list[Flock], zones: list[Zone], adj_z: dict[Zone, list[Zone]], adj_e: dict[Specie, list[Specie]]):
        if flocks and adj_e and adj_z:
            distribution = CSP(flocks, zones, adj_z, adj_e)
            for item in distribution.items():
                item[0].asign_zone(item[1])

    def max_probability(self, birth: bool):
        min = 2
        max = -1
        output = None
        for zone in self.zones:
            for flock in zone.flocks:
                if zone.total == 0:
                    if birth: current=1
                    else:  current=0
                else: current = flock.total/zone.total
                if birth and current < min:
                    output = flock
                    min = current
                if not birth and current > max:
                    output = flock
                    max = current
        return output
