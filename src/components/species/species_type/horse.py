from ..specie import *

class Horse(Specie):
    name = 'horse'

    @staticmethod
    def life_expectancy():
        pass
    
    @staticmethod
    def habitat():
        return [Habitat.Tropical, Habitat.Desertic]
    
    @staticmethod
    def nutrition():
        return Nutrition.Herbivore
    
    @staticmethod
    def fertility_level():
        pass
    
    @staticmethod
    def gestation_time():
        pass  
    
    @staticmethod
    def speed():
        pass

    @staticmethod
    def reach():
        pass

    @staticmethod
    def vision():
        pass