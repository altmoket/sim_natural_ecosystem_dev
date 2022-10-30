from species.base import Specie
from species.characteristics import Nutrition

class T_Rex(Specie):

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
