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
    def feeding(): raise NotImplementedError() # De que se alimenta


class BengalTiger(Species):
    name = Specie.bengal_tiger
    def life_expectancy(): pass
    def habitat(): return [PolarHabitat, TemperedHabitat]
    def nutrition(): return Carnivorous
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass
    def feeding(): pass


class GrizzlyBear(Species):
    name = Specie.grizzly_bear
    def life_expectancy(): pass
    def habitat(): return [TropicalHabitat, DeserticHabitat]
    def nutrition(): return Carnivorous
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass
    def feeding(): pass


class Horse(Species):
    name = Specie.horse
    def life_expectancy(): pass
    def habitat(): return [TropicalHabitat, DeserticHabitat]
    def nutrition(): return Herbivore
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass
    def feeding(): pass


class PolarBear(Species):
    name = Specie.polar_bear
    def life_expectancy(): pass
    def habitat(): return [PolarHabitat, TemperedHabitat]
    def nutrition(): return Carnivorous
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): return 40 # Km x Hora
    def reach(): pass
    def vision(): pass
    def feeding(): return [Specie.seal]


class Rabbit(Species):
    name = Specie.rabbit
    def life_expectancy(): pass
    def habitat():return [TropicalHabitat, DeserticHabitat, TemperedHabitat, PolarHabitat]
    def nutrition(): return Herbivore
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass
    def feeding(): pass


class Tiger(Species):
    name = Specie.tiger
    def life_expectancy(): pass
    def habitat(): return [TropicalHabitat]
    def nutrition(): return Carnivorous
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass
    def feeding(): pass
    
class Ant(Species):
    name = Specie.ant
    def life_expectancy(): pass
    def habitat(): return [DeserticHabitat, TropicalHabitat]
    def nutrition(): return Herbivore
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass
    def feeding(): pass
    
class Seal(Species):
    name = Specie.seal
    def life_expectancy(): pass
    def habitat(): return [PolarHabitat]
    def nutrition(): return Carnivorous
    def fertility_level(): pass
    def gestation_time(): pass
    def speed(): pass
    def reach(): pass
    def vision(): pass
    def feeding(): pass