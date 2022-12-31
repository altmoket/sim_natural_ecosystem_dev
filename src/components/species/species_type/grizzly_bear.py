from ..specie import *

class GrizzlyBear(Specie):
    name = 'grizzly bear'

    @staticmethod
    def life_expectancy():
        pass
        
    @staticmethod
    def habitat():
        return [Habitat.Tropical, Habitat.Desertic]
        
    @staticmethod
    def nutrition():
        return Nutrition.Carnivorous
        
    @staticmethod
    def fertility_level():
        pass
        
    @staticmethod
    def gestation_time():
        pass  
        
    @staticmethod
    def speed():
        pass