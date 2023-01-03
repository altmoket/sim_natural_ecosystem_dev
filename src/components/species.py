from .utils import *

class Species:
    name = Specie.base

    @classmethod
    def search_specie_type(self, name: property):
        for cls in self.__subclasses__():
            if cls.name == name:
                return cls
        raise Exception("Unknown Specie")

    def life_expectancy(): raise NotImplementedError()
    def habitat(): raise NotImplementedError()
    def nutrition(): raise NotImplementedError()
    def fertility_level(): raise NotImplementedError()
    def gestation_time(): raise NotImplementedError()
    def speed(): raise NotImplementedError()
    def reach(): raise NotImplementedError()
    def vision(): raise NotImplementedError()


class BengalTiger(Species):
    name = Specie.bengal_tiger
    def life_expectancy(): pass
    def habitat(): return [Habitat.polar, Habitat.tempered]
    def nutrition(): return Nutrition.carnivorous
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass


class GrizzlyBear(Species):
    name = Specie.grizzly_bear
    def life_expectancy(): pass
    def habitat(): return [Habitat.tropical, Habitat.desertic]
    def nutrition(): return Nutrition.carnivorous
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass


class Horse(Species):
    name = Specie.horse
    def life_expectancy(): pass
    def habitat(): return [Habitat.tropical, Habitat.desertic]
    def nutrition(): return Nutrition.herbivore
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass


class PolarBear(Species):
    name = Specie.polar_bear
    def life_expectancy(): pass
    def habitat(): return [Habitat.polar, Habitat.tempered]
    def nutrition(): return Nutrition.carnivorous
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass


class Rabbit(Species):
    name = Specie.rabbit
    def life_expectancy(): pass
    def habitat():return [Habitat.tropical, Habitat.desertic, Habitat.tempered, Habitat.polar]
    def nutrition(): return Nutrition.herbivore
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass


class Tiger(Species):
    name = Specie.tiger
    def life_expectancy(): pass
    def habitat(): return [Habitat.tropical]
    def nutrition(): return Nutrition.carnivorous
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass
    
class Ant(Species):
    name = Specie.ant
    def life_expectancy(): pass
    def habitat(): return [Habitat.desertic, Habitat.tropical]
    def nutrition(): return Nutrition.herbivore
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass