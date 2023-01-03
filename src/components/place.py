import random
from .utils import Habitat
type_temperature = {Habitat.tropical: (17, 26), Habitat.desertic: (
    27, 35), Habitat.polar: (-5, 10), Habitat.tempered: (6, 18)}


class Zone:
    def __init__(self, _id: int, zone_type):
        self.id = _id
        self.type = zone_type
        self.temperature_range = type_temperature[self.type]
        self.__temperature__ = None
        self.flocks: list[Flock] = []

    def get_temperature(self):
        t_min, t_max = self.temperature_range
        self.__temperature__ = round(random.uniform(t_min, t_max), 2)
        return self.__temperature__

    def add_flock(self, flock):
        self.flocks.append(flock)
        
    def __repr__(self) -> str:
        return str(self.id)

    @property
    def total(self):
        total = 0
        for flock in self.flocks:
            total += flock.total
        return total


class Flock:
    def __init__(self, type: str, female_total: int = 0, male_total: int = 0):
        self.female_total = female_total
        self.male_total = male_total
        self.__type__ = type
        self.zone = None

    @property
    def total(self):
        return self.female_total + self.male_total

    def asign_zone(self, zone: Zone):
        zone.add_flock(self)
        self.zone = zone

    def add_animal(self, sex: int):
        if sex == 0:
            self.male_total += 1
        else:
            self.female_total += 1

    def remove_animal(self, sex: int):
        if sex == 0:
            self.male_total -= 1
        else:
            self.female_total -= 1


class Behavior:
    group = 'group'
    individual = 'individual'


class Entity:
    behavior: Behavior = None

    def __init__(self) -> None:
        self.members = {}
        self.member = None

    def all(self):
        if self.behavior == Behavior.individual:
            return self.member
        if self.behavior == Behavior.group:
            return self.members


class Group(Entity):
    behavior = Behavior.group

    def __init__(self, behavior: str = Behavior.group) -> None:
        self.behavior = behavior
        super().__init__()

    def create_subgroup(self, member_type: str, is_individual: bool = False):
        if not self.exist_subgroup(member_type):
            self.subgroups[member_type]

    def exist_subgroup(self, member_type: str):
        return self.subgroups[member_type] is not None

    def add_member(self, member_type: str):
        pass

    def remove_member(self, member_type: str):
        pass

    def remove_individual_member(self, member_type: str, id: int):
        pass

    def add_individual_member(self, member_type: str, gender: str):
        pass


class Individual(Entity):
    behavior = Behavior.individual

    def __init__(self, id: int, type: str, gender: str) -> None:
        pass


class Hive(Group):
    pass
