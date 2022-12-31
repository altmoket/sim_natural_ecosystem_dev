from ..specie import *

class PolarBear(Specie):
    name = 'polar bear'

    @staticmethod
    def life_expectancy():
        pass
        
    @staticmethod
    def habitat():
        return [Habitat.Polar, Habitat.Tempered]
        
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