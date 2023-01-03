from src import *

def main():
    flock1 = Flock(Specie.bengal_tiger, 10, 12)
    flock2 = Flock(Specie.grizzly_bear, 12, 15)
    flock3 = Flock(Specie.rabbit, 20, 10)
    flock4 = Flock(Specie.tiger, 12, 13)
    flock5 = Flock(Specie.polar_bear, 12, 15)
    flock6 = Flock(Specie.bengal_tiger, 13, 15)
    flock7 = Flock(Specie.horse, 16, 20)
    flocks = [flock1, flock2, flock3, flock4, flock5, flock6, flock7]

    zones, adj_z = WorldGenerator().generate(3, 7)
    print('Zones')
    [print(f'{zone}') for zone in zones]

    print('\nMap')
    [print(f'{zone} with {adj}') for zone, adj in adj_z.items()]

    adj_e = {Specie.tiger: [Specie.grizzly_bear, Specie.horse],
             Specie.polar_bear: [Specie.bengal_tiger],
             Specie.bengal_tiger: [Specie.rabbit],
             Specie.grizzly_bear: [Specie.tiger, Specie.rabbit],
             Specie.rabbit: [], Specie.horse: []}
    eco = Ecosystem(zones, flocks=flocks, adj_z=adj_z, adj_e=adj_e)
    solution = eco.zones
    print('\nCSP')
    for item in solution:
        print(f'{item} : {[flock.__type__ for flock in item.flocks]}')

    print('\nSimulation')
    sim = Simulator(eco, 30)
    sim.simulate()

if __name__ == "__main__":
    main()