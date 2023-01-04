class Specie:
    base = 'base'
    bengal_tiger = 'bengal tiger'
    grizzly_bear = 'grizzly bear'
    horse = 'horse'
    polar_bear = 'polar bear'
    rabbit = 'rabbit'
    tiger = 'tiger'
    ant = 'ant'
    seal = 'seal'
    fish = 'fish'


class Habitat:
    __type__ = "base"


class TropicalHabitat(Habitat):
    __type__ = "tropical"


class DeserticHabitat(Habitat):
    __type__ = "desertic"


class PolarHabitat(Habitat):
    __type__ = "polar"


class TemperedHabitat(Habitat):
    __type__ = "tempered"


class Nutrition:
    __type__ = "base"
    
class Herbivore(Nutrition):
    __type__ = 'herbivore'
    
class Carnivorous(Nutrition):
    __type__ = 'carnivorous'


if __name__ == "__main__":
    print(TropicalHabitat.name)
