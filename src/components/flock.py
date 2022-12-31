from ..utils import characteristics
#from .zone import Zone
class Flock:
    def __init__(self,type:str,zone,female_total:int=0,male_total:int=0):
        self.female_total=female_total
        self.male_total=male_total
        self.__type__=type
        self.zone=zone

    @property
    def total(self):
         return self.female_total+self.male_total

    def add_animal(self,sex:int):
        if sex == 0:
            self.male_total+=1
        else: self.female_total+=1

    def remove_animal(self,sex:int):
        if sex == 0:
            self.male_total-=1
        else: self.female_total-=1