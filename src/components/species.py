from .utils import *


# class Species:
#     name = Specie.base

#     @classmethod
#     def search_specie_type(self, name: property):
#         for cls in self.__subclasses__():
#             if cls.name == name:
#                 return cls
#         raise Exception("Unknown Specie")

#     def life_expectancy(): raise NotImplementedError()
#     def habitat(): raise NotImplementedError()
#     def nutrition(): raise NotImplementedError()
#     def fertility_level(): raise NotImplementedError()
#     def gestation_time(): raise NotImplementedError()
#     def speed(): raise NotImplementedError()
#     def reach(): raise NotImplementedError()
#     def vision(): raise NotImplementedError()
#     def feeding(): raise NotImplementedError()  # De que se alimenta


class GrizzlyBear(Specie):
    name = 'grizzly bear'
    life_expectancy = None
    habitat = [TropicalHabitat, DeserticHabitat]
    nutrition = Carnivorous
    fertility_level = None
    gestation_time = None
    speed = None
    reach = None
    vision = None
    feeding = None


class Horse(Specie):
    name = "horse"
    life_expectancy = None
    habitat = [TropicalHabitat, DeserticHabitat]
    nutrition = Herbivore
    fertility_level = None
    gestation_time = None
    speed = None
    reach = None
    vision = None
    feeding = None


class Rabbit(Specie):
    name = "rabbit"
    life_expectancy = None
    habitat = [TropicalHabitat, DeserticHabitat, TemperedHabitat, PolarHabitat]
    nutrition = Herbivore
    fertility_level = None
    gestation_time = None
    speed = None
    reach = None
    vision = None
    feeding = None


class Tiger(Specie):
    name = "tiger"
    life_expectancy = None
    habitat = [TropicalHabitat]
    nutrition = Carnivorous
    fertility_level = None
    gestation_time = None
    speed = None
    reach = None
    vision = None
    feeding = None


class BengalTiger(Tiger):
    name = 'bengal tiger'
    life_expectancy = None
    habitat = [PolarHabitat, TemperedHabitat]
    nutrition = Carnivorous
    fertility_level = None
    gestation_time = None
    speed = None
    reach = None
    vision = None
    feeding = None


class Ant(Specie):
    name = 'ant'
    life_expectancy = None
    habitat = [DeserticHabitat, TropicalHabitat]
    nutrition = Herbivore
    fertility_level = None
    gestation_time = None
    speed = None
    reach = None
    vision = None
    feeding = None


class Seal(Specie):
    name = 'seal'
    life_expectancy = None
    habitat = [PolarHabitat]
    nutrition = Carnivorous
    fertility_level = None
    gestation_time = None
    speed = None
    reach = None
    vision = None
    feeding = None


class PolarBear(Specie):
    name = 'polar bear'
    life_expectancy = None
    habitat = [PolarHabitat, TemperedHabitat]
    nutrition = Carnivorous
    fertility_level = None
    gestation_time = None
    speed = 40
    reach = None
    vision = None
    feeding = [Seal]
