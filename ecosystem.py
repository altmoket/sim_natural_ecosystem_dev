from enum import Enum
from subprocess import call
# from symbol import return_stmt
import networkx as nx
import species as sp
class Ecosystem:
    species=nx.DiGraph()
    
    @property
    def total_of_animals(self):
        return self.Total_of_animals
    @property   
    def total_of_species(self):
        return self.Total_of_species
    @property
    def total_of_animals_of(self,species):
        return len(self.species.nodes[species]['animals'])

    def __init__(self):
        self.Total_of_animals=0
        self.Total_of_species=0
    
    def add_specie(self,specie_name,a_threat_to,threatened_by):
            if(not specie_name in self.species.nodes):
                self.species.add_node(specie_name,animals=[])
                for species in threatened_by:
                    self.species.add_edge(species,specie_name)
                for species in a_threat_to:
                    self.species.add_edge(species,a_threat_to)
                self.Total_of_species+=1
            else:
                print("This species is already on the Ecosystem")
    
    def add_animal(self,animal,species_name):
        self.species.nodes[species_name]['animals'].append(animal)
        self.Total_of_animals +=1
