from src import *

def main():  
    animals=[Tiger(0),Tiger(0),Tiger(1),Rabbit(1),GrizzlyBear(0),PolarBear(1),GrizzlyBear(0),Horse(0),Rabbit(0),
            Horse(1),Horse(1),BengalTiger(1),GrizzlyBear(0),Tiger(1),Rabbit(0),GrizzlyBear(1),BengalTiger(1),
            PolarBear(0),Horse(0),BengalTiger(0),GrizzlyBear(1),Horse(0),Tiger(1),Rabbit(1),PolarBear(0),PolarBear(0)]
    print('Zones')
    zones, adj_z = WorldGenerator().generate(8, 8)

    print('\nMap')
    [print(f'{zone} adj {adj}') for zone, adj in adj_z.items()]

    adj_e = {Specie.tiger: [Specie.grizzly_bear, Specie.horse],
             Specie.polar_bear: [Specie.bengal_tiger],
             Specie.bengal_tiger: [Specie.rabbit],
             Specie.grizzly_bear: [Specie.tiger, Specie.rabbit],
             Specie.rabbit: [], Specie.horse: []}
    eco = Ecosystem(zones, animals=animals, adj_z=adj_z, adj_e=adj_e)
    solution = eco.zones
    
    print('\nCSP')
    for item in solution:
        print(f'{item} : {list(item.species.keys())}')

    print('\nA*')
    prob = MigrationProblem(solution[0], Habitat.tropical)
    result = astar_tree_search(prob)
    actions = path_states(result) 
    print(actions)

    print('\nSimulation')
    sim = Simulator(eco, 12, 2) # Dias / Años
    sim.simulate()

#class test:
#    def __init__(self):
#         prob = MigrationProblem(solution[0], Habitat.tropical)
#    result = astar_tree_search(prob,h)
#    actions = path_states(result) 
#    print(actions)
#    def h(self, node): # Esto hay que llenarlo         
#        zone:Zone=node.state
#        result=0
#        for _, (female,male)  in zone.species.items():
#            animals=female+male
#            if len(animals)>0 and self.goal in animals[0].habitat():
#                result+=len(animals)
#        return zone.total - result    
    
if __name__ == "__main__":
    main()