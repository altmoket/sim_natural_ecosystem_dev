from src import WorldGenerator
import random

class TestWorldGenerator:
    generator = WorldGenerator()
    
    def test_generate_habitat(self):
        habitats = []
        for _ in range(10):
            habitat = random.choice(self.generator.habitats)
            habitats.append(habitat)
        assert len(habitats) == 10
        
    def test_generate_zone(self):
        zones = []
        for i in range(10):
            zones.append(self.generator.generate_zone(i))
        assert len(zones) == 10
        
    def test_generate_zones(self):
        zones = self.generator.generate_zones(6)
        assert len(zones) == 6
        
    def test_generate(self):
        zones = self.generator.generate(3, 6)
        print(zones)
        assert True
        
    def test_distances_among_zones(self):
        zones, adjacent_z = self.generator.generate(3,15)
        for zone in zones:
            for adj, distance in zone.distance_adj_z.items():
                print(f"({str(zone)}) -> ({str(adj)}) ------- {distance}")
        assert True
        