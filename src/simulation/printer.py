

from src.components.species import Species
from src.components import Zone

class AnimalActionPrinter:
    def __init__(self, animal: Species = None) -> None:
        self.animal = animal
    
    def feed_vegetation(self):
        return f"Animal {self.animal} feeds on the vegetation in its zone"
    
    def looking_for_food(self, zone: Zone):
        return f"Animal {self.animal} went to find food to {zone}"
        
    def eat_animal_in_zone(self, prey: Species, zone: Zone):
        return f"Animal {self.animal} ate animal {prey} in {zone}"
    
    def start_migration(self, zone: Zone):
        return f"Animal {self.animal} began to migrate to {zone}"
    
    def arrive_to_zone(self, zone:Zone):
        return f"Animal {self.animal} arrived at {zone}"
    
    def died_eaten(self):
        return f"Animal {self.animal} died because he was eaten"
    
    def died_by_natural_effect(self):
        return f"Animal {self.animal} died because he reached the end of his life"
    
    def died_by_low_health(self):
        return f"Animal {self.animal} died because his health is too low"
    