from src import *

def main():  
    animals=[Tiger(0),Tiger(0),Tiger(1),Rabbit(1),GrizzlyBear(0),PolarBear(1),GrizzlyBear(0),Horse(0),Rabbit(0),Ant(0),Ant(1),
            Horse(1),Horse(1),BengalTiger(1),GrizzlyBear(0),Tiger(1),Rabbit(0),GrizzlyBear(1),BengalTiger(1),Ant(0),Ant(0),Ant(1),
            PolarBear(0),Horse(0),BengalTiger(0),GrizzlyBear(1),Horse(0),Tiger(1),Rabbit(1),PolarBear(0),PolarBear(0),Ant(1)]
    print('Zones')
    zones = WorldGenerator().generate(8, 8)

    print('\nMap')
    [print(f'{zone} adj {zone.adj_z}') for zone in zones]

    eco = Ecosystem(zones, animals=animals)
    solution = eco.zones
    
    print('\nCSP')
    for item in solution:
        print(f'{item} : {list(item.species.keys())}')

    #print('\nA*') 
    #tiger = Tiger(0)
    #path,_ = tiger.migrate_weight((3,solution[0])) 
    #print(path)

    print(len(animals))
    print('\nSimulation')
    sim = Simulator(eco, 12, 3) # Dias / Años
    sim.simulate()
    print(sim.ecosystem.total_of_animals)

    
if __name__ == "__main__":
    main()