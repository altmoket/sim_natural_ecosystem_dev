from .flock import Flock
class Zone:
    def __init__(self):
        self.flocks=[]
    @property
    def total(self):
        total=0
        for flock in self.flocks:
            total+=flock.total
        return total
    def add_flock(self,flock):
        self.flocks.append(flock)

        
