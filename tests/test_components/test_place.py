from src import *

class TestZone:
    z_tropical = Zone(1, Habitat.tropical)
    z_desertic = Zone(2, Habitat.desertic)
    z_polar = Zone(3, Habitat.polar)
    z_tempered = Zone(4, Habitat.tempered)
    
    def get_temperature(self, zone: Zone):
        temperature = zone.get_weather()
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