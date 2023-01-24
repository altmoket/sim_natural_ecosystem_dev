from src import *

def main():
    
    
    animals=[Tiger(0),Tiger(1),Tiger(1),GrizzlyBear(0),GrizzlyBear(0),Horse(0),Horse(1),Horse(1),BengalTiger(1),GrizzlyBear(0),
            Tiger(1),Rabbit(0),GrizzlyBear(0),BengalTiger(1),PolarBear(0),Horse(1),GrizzlyBear(1)]
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

    print('\nSimulation')
    sim = Simulator(eco, 50)
    sim.simulate()

if __name__ == "__main__":
    main()