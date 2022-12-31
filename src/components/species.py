from .utils import *

class Specie:
    name = 'base'

    @classmethod
    def search_qry_type(self, name: str):
        cls = {}
        for _cls in self.__subclasses__(): 
            cls[_cls.name] = _cls
        if not name in cls: raise Exception("Unknown Specie")
        return cls[name]

    def life_expectancy():raise NotImplementedError() 
    def habitat():raise NotImplementedError()
    def nutrition():raise NotImplementedError()  
    def fertility_level():raise NotImplementedError()    
    def gestation_time():raise NotImplementedError()    
    def speed():raise NotImplementedError()   
    def reach():raise NotImplementedError()  
    def vision():raise NotImplementedError()


class BengalTiger(Specie):
    name = 'bengal tiger'

    def life_expectancy():pass   
    def habitat():return [Habitat.Polar, Habitat.Tempered]      
    def nutrition():return Nutrition.Carnivorous       
    def fertility_level():pass   
    def gestation_time():pass         
    def speed():pass
    def reach():pass
    def vision():pass


class GrizzlyBear(Specie):
    name = 'grizzly bear'

    def life_expectancy():pass      
    def habitat():return [Habitat.Tropical, Habitat.Desertic]     
    def nutrition():return Nutrition.Carnivorous        
    def fertility_level():pass      
    def gestation_time():pass  
    def speed():pass
    def reach():pass
    def vision():pass


class Horse(Specie):
    name = 'horse'

    def life_expectancy():pass
    def habitat():return [Habitat.Tropical, Habitat.Desertic]
    def nutrition():return Nutrition.Herbivore
    def fertility_level():pass
    def gestation_time():pass  
    def speed():pass
    def reach():pass
    def vision():pass


class PolarBear(Specie):
    name = 'polar bear'

    def life_expectancy():pass
    def habitat():return [Habitat.Polar, Habitat.Tempered]
    def nutrition():return Nutrition.Carnivorous
    def fertility_level():pass
    def gestation_time():pass  
    def speed():pass
    def reach():pass
    def vision():pass


class Rabbit(Specie):
    name = 'rabbit'

    def life_expectancy():pass
    def habitat():return [Habitat.Tropical, Habitat.Desertic, Habitat.Tempered]
    def nutrition():return Nutrition.Herbivore
    def fertility_level():pass
    def gestation_time():pass  
    def speed():pass
    def reach():pass
    def vision():pass


class Tiger(Specie):
    name = 'tiger'
    
    def life_expectancy():pass
    def habitat():return [Habitat.Tropical]
    def nutrition():return Nutrition.Carnivorous
    def fertility_level():pass
    def gestation_time():pass  
    def speed():pass
    def reach():pass
    def vision():pass