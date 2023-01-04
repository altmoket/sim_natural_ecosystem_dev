class Specie:
    # base = 'base'
    # bengal_tiger = 'bengal tiger'
    # grizzly_bear = 'grizzly bear'
    # horse = 'horse'
    # polar_bear = 'polar bear'
    # rabbit = 'rabbit'
    # tiger = 'tiger'
    # ant = 'ant'
    # seal = 'seal'
    # fish = 'fish'
    name = "base"
    life_expectancy = None
    habitat = None
    nutrition = None
    fertility_level = None
    gestation_time = None
    speed = None
    reach = None
    vision = None
    feeding = None  # De quien se alimenta

    @classmethod
    def search_specie_type(self, name: property):
        def find_class_than_match_property(cls, name: property):
            if cls.name == name:
                return cls
            for subclass in cls.__subclasses__():
                subclass = find_class_than_match_property(subclass, name)
                if subclass is not None:
                    return subclass
            return None

        subclass = find_class_than_match_property(self, name)
        if subclass is not None:
            return subclass
        raise Exception("Unknown Specie")


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
