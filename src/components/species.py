from .utils import Habitat,Specie

class Species:
    name = Specie.base

    @classmethod
    def search_specie_type(self, name: property):
        for cls in self.__subclasses__():
            if cls.name == name:
                return cls
        raise Exception("Unknown Specie")

    def habitat(): raise NotImplementedError()
    def feed_on_vegetation(): raise NotImplementedError()
    def life_expectancy(): raise NotImplementedError()
    def speed(): raise NotImplementedError()
    def attack_power(): raise NotImplementedError()
    def defense_power(): raise NotImplementedError()


class BengalTiger(Species):
    name = Specie.bengal_tiger
    def habitat(): return [Habitat.polar, Habitat.tempered]
    def feed_on_vegetation(): return False
    def life_expectancy(): return (20,26)
    def speed(): pass
    def attack_power(): pass
    def defense_power(): pass


class GrizzlyBear(Species):
    name = Specie.grizzly_bear
    def habitat(): return [Habitat.tropical, Habitat.desertic]
    def feed_on_vegetation(): return False
    def life_expectancy(): return (20,30)
    def speed(): pass
    def attack_power(): pass
    def defense_power(): pass


class Horse(Species):
    name = Specie.horse
    def habitat(): return [Habitat.tropical, Habitat.desertic]
    def feed_on_vegetation(): return True
    def life_expectancy(): return (25,30)
    def speed(): pass
    def attack_power(): pass
    def defense_power(): pass


class PolarBear(Species):
    name = Specie.polar_bear
    def habitat(): return [Habitat.polar, Habitat.tempered]
    def feed_on_vegetation(): return True
    def life_expectancy(): return (20,25)
    def speed(): pass
    def attack_power(): pass
    def defense_power(): pass


class Rabbit(Species):
    name = Specie.rabbit
    def habitat():return [Habitat.tropical, Habitat.desertic, Habitat.tempered, Habitat.polar]
    def feed_on_vegetation(): return True
    def life_expectancy(): return (7,9)
    def speed(): pass
    def attack_power(): pass
    def defense_power(): pass


class Tiger(Species):
    name = Specie.tiger
    def habitat(): return [Habitat.tropical]
    def feed_on_vegetation(): return False
    def life_expectancy(): return (8,10)
    def speed(): pass
    def attack_power(): pass
    def defense_power(): pass
    
    
class Ant(Species):
    name = Specie.ant
    def habitat(): return [Habitat.desertic, Habitat.tropical]
    def feed_on_vegetation(): return True
    def life_expectancy(): return (1,2)
    def speed(): pass
    def attack_power(): pass
    def defense_power(): pass