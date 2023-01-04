from src import *
from src.components.species import *

def main():
    flock1 = Flock(BengalTiger, 10, 12)
    flock2 = Flock(GrizzlyBear, 12, 15)
    flock3 = Flock(Rabbit, 20, 10)
    flock4 = Flock(Tiger, 12, 13)
    flock5 = Flock(PolarBear, 12, 15)
    flock6 = Flock(BengalTiger, 13, 15)
    flock7 = Flock(Horse, 16, 20)
    flocks = [flock1, flock2, flock3, flock4, flock5, flock6, flock7]

    zones, adj_z = WorldGenerator().generate(3, 7)
    print('Zones')
    [print(f'{zone}') for zone in zones]

    print('\nMap')
    [print(f'{zone} with {adj}') for zone, adj in adj_z.items()]

    adj_e = {Tiger: [GrizzlyBear, Horse],
             PolarBear: [BengalTiger],
             BengalTiger: [Rabbit],
             GrizzlyBear: [Tiger, Rabbit],
             Rabbit: [], Horse: []}
    eco = Ecosystem(zones, flocks=flocks, adj_z=adj_z, adj_e=adj_e)
    solution = eco.zones
    print('\nCSP')
    for item in solution:
        print(f'{item} : {[flock.__type__.name for flock in item.flocks]}')

    print('\nSimulation')
    sim = Simulator(eco, 30)
    sim.simulate()

if __name__ == "__main__":
    main()