from ..components.zone import Zone
class Ecosystem:
    def __init__(self,zones:list[Zone]):
        self.zones=zones
        self.total_of_animals = 0
        for zone in self.zones:
            self.total_of_animals += zone.total
    
    def max_probability(self,birth:bool):
        min=2
        max=-1
        output= None
        for zone in self.zones:
            for flock in zone.flocks:
                current=flock.total/zone.total
                if birth and current < min :
                    output=flock
                    min=current
                if not birth and current > max:
                    output=flock
                    max=current
        return output