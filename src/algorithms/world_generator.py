import random
from src.components import Zone
from src.components.utils import *
from collections import defaultdict

class WorldGenerator:
    def __init__(self) -> None:
        self.habitats = [Habitat.tropical, Habitat.desertic,Habitat.polar, Habitat.tempered]
        
    def random(self, min, max):
        try:
            if min > max: return 0
            return random.randint(min, max)
        except:
            print("Min and Max:")
            print(min, max)
            raise "Error generando random"

    def generate(self, min_number_of_zones, max_number_of_zones):
        number_of_zones = self.random(
            min_number_of_zones, max_number_of_zones)

        zones = self.generate_zones(number_of_zones)

        adjacent_zones = self.generate_adjacent_zones(zones)
        
        self.assign_distance_among_zones(zones)

        return zones  # Vertices, Aristas

    def generate_zones(self, number_of_zones: int) -> list[Zone]:
        return [self.generate_zone(id=i) for i in range(number_of_zones)]

    def generate_zone(self, id: int) -> Zone:
        habitat = random.choice(self.habitats)
        return Zone(id, habitat)

    def generate_adjacent_zones(self, zones: list[Zone]):
        number_of_zones = len(zones)
        adjacent_zones:dict[Zone,list[Zone]] = defaultdict(list)
        
        for i in range(number_of_zones):
            adjacent_zones = self.generate_adjacent_zones_to_zone_i_and_update_adjacent_zones(
                zones, adjacent_zones, i)
        
        return adjacent_zones

    def generate_adjacent_zones_to_zone_i_and_update_adjacent_zones(self, zones: list[Zone], adjacent_zones: dict[Zone,list[Zone]], i: int):
        adjacent_zones_to_zone_i = self.generate_adjacent_zones_to_zone_i(
            zones, i, adjacent_zones)
        adjacent_zones = self.update_adjacent_zones(
            zones[i], adjacent_zones, adjacent_zones_to_zone_i)
        for zone in zones: zone.adj_z = {adj_zone:0 for adj_zone in adjacent_zones[zone]} 
        return adjacent_zones

    def generate_adjacent_zones_to_zone_i(self, zones: list[Zone], id: int, adjacent_zones: dict[Zone,list[Zone]]):
        avaliable_zones = self.get_avaliable_zones(zones, id, adjacent_zones)
        number_of_adjacent_zones = self.random(1, len(avaliable_zones)-1)

        adjacent_zone = []
        while number_of_adjacent_zones > 0:
            zone_number = self.random(0, number_of_adjacent_zones - 1)
            zone = avaliable_zones.pop(zone_number)
            adjacent_zone.append(zone)
            number_of_adjacent_zones -= 1

        return adjacent_zone

    def get_avaliable_zones(self, zones: list, id, adjacent_zones):
        zones_copy = zones.copy()
        zone = zones_copy.pop(id)

        zones_copy_set = set(zones_copy)
        adjacent_zones_set_in_id = set(adjacent_zones[zone])

        return list(zones_copy_set.difference(adjacent_zones_set_in_id))

    def update_adjacent_zones(self, zone: Zone, adjacent_zones: dict[Zone, list[Zone]], adjacent_zones_to_zone_i:list[Zone]):
        adjacent_zones[zone] += adjacent_zones_to_zone_i
        for adjacent_zone in adjacent_zones_to_zone_i:
            adjacent_zones[adjacent_zone].append(zone)
        return adjacent_zones
    
    def assign_distance_among_zones(self, zones: list[Zone]):
        for zone in zones:
            for adj,d in zone.adj_z.items():
                if d==0 :
                    distance = self.random(1, 15)
                    zone.adj_z[adj] = distance
                    adj.adj_z[zone] = distance