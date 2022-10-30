from species.base import Specie
from species.characteristics import Habitat, Nutrition

class  Velociraptors(Specie):
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
