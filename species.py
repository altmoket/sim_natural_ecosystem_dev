from enum import Enum
from subprocess import call
from symbol import return_stmt
import networkx as nx
class Species:
    @property
    def health_state(self):
        return self.Health_state
    @property
    def sex(self):
        return self.Sex
    @property
    def location(self):
        return self.Location
    @property
    def age(self):
        return self.Age
    @property
    def defense_level(self):
        return self.Defense_level
    @property
    def attack_level(self):
        return self.Attack_level
    @staticmethod
    def life_expectancy():
        pass 
    @staticmethod
    def habitat():
        pass
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
        return 10
    @staticmethod
    def vision():
        pass
    @staticmethod
    def nutrition():
       pass

    def __init__(self,location,sex=1,defense_level=0,attack_level=0):
         self.Sex=sex
         self.Age=0
         self.Health_state=Health_States.Optimum
         self.Defense_level=defense_level
         self.Attack_level=attack_level
         self.Location=location

Health_States = Enum('Health_States','Healthy Sick')

Sex = Enum('Sex','Female' 'Male')

Habitat = Enum('Habitat','Aerial Land Maritime')

Nutrition  = Enum('Nutrition','Herbivore Carnivorous')

class Brachiosaurus(Species):
        @staticmethod
        def life_expectancy():
            pass
        @staticmethod
        def habitat():
            return Habitat.Land
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
class Triceraptops(Species):
        @staticmethod
        def life_expectancy():
            pass
        @staticmethod
        def habitat():
            pass
        @staticmethod
        def fertility_level():
            pass
        @staticmethod
        def gestation_time():
            pass  
        @staticmethod
        def nutrition():
            return Nutrition.Herbivore
        @staticmethod
        def speed():
            pass
class  Velociraptors(Species):
        @staticmethod
        def life_expectancy():
            pass

        @staticmethod
        def habitat():
            return Habitat.Land

        @staticmethod
        def fertility_level():
            pass

        @staticmethod
        def gestation_time():
            pass  

        @staticmethod
        def nutrition():
            return Nutrition.Carnivorous

        @staticmethod
        def speed():
            return 39

class Pterodactilos(Species):
        @staticmethod
        def life_expectancy():
            pass
        @staticmethod
        def habitat():
            pass
        @staticmethod
        def fertility_level():
            pass
        @staticmethod
        def gestation_time():
            pass  

        @staticmethod
        def nutrition():
            pass
        @staticmethod
        def speed():
            pass
class T_Rex(Species):

        @staticmethod
        def life_expectancy():
            return 30

        @staticmethod
        def habitat():
            pass

        @staticmethod
        def fertility_level():
            pass

        @staticmethod
        def gestation_time():
            pass  

        @staticmethod
        def nutrition():
            return Nutrition.Carnivorous
        @staticmethod
        def speed():
            pass