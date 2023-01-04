from src import *
from src.components.utils.tools import *

class TestZone:
    z_tropical = Zone(1, TropicalHabitat)
    z_desertic = Zone(2, DeserticHabitat)
    z_polar = Zone(3, PolarHabitat)
    z_tempered = Zone(4, TemperedHabitat)
    
    def get_temperature(self, zone: Zone):
        temperature = zone.get_temperature()
        return temperature
    
    def test_tropical_temperature(self):
        temperature = self.get_temperature(self.z_tropical)
        print(temperature)
        assert 0 == 0
    
    def test_desertic_temperature(self):
        temperature = self.get_temperature(self.z_desertic)
        print(temperature)
        assert 0 == 0
    
    def test_polar_temperature(self):
        temperature = self.get_temperature(self.z_polar)
        print(temperature)
        assert 0 == 0
    
    def test_tempered_temperature(self):
        temperature = self.get_temperature(self.z_tempered)
        print(temperature)
        assert 0 == 0
        
class TestFlock:
    pass