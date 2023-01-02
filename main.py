from src import *

# PARA FACILIDAD EN LA SIMULACION GENERANDO ZONAS, MANADAS
# Y UBICANDOLAS SATISFACTORIAMENTE EN ZONAS SEGUN CSP


def main():
    zone1 = Zone(1, Habitat.tropical)
    zone2 = Zone(2, Habitat.tempered)
    zone3 = Zone(3, Habitat.tropical)
    zone4 = Zone(4, Habitat.desertic)
    flock1 = Flock(Specie.horse, 34, 13)
    flock2 = Flock(Specie.tiger, 34, 13)
    flock3 = Flock(Specie.grizzly_bear, 32, 45)
    flock4 = Flock(Specie.horse, 21, 14)
    flock5 = Flock(Specie.horse, 12, 23)
    flock1.asign_zone(zone1)
    flock2.asign_zone(zone1)
    flock3.asign_zone(zone2)
    flock4.asign_zone(zone3)
    flock5.asign_zone(zone3)
    eco = Ecosystem([zone1, zone2, zone3, zone4])
    sim = Simulator(eco, 30)
    sim.simulate()

    print('CSP')
    flock1 = Flock(Specie.bengal_tiger)
    flock2 = Flock(Specie.grizzly_bear)
    flock3 = Flock(Specie.rabbit)
    flock4 = Flock(Specie.tiger)
    flock5 = Flock(Specie.polar_bear)
    flock6 = Flock(Specie.bengal_tiger)
    flock7 = Flock(Specie.horse)
    flocks = [flock1, flock2, flock3, flock4, flock5, flock6, flock7]

    zone1 = Zone(1, Habitat.tempered)
    zone2 = Zone(2, Habitat.desertic)
    zone3 = Zone(3, Habitat.tropical)
    zone4 = Zone(4, Habitat.polar)
    zones = [zone1, zone2, zone3, zone4]

    adj_z = {zone1: [zone2],
             zone2: [zone1, zone4],
             zone3: [zone4],
             zone4: [zone3, zone2]}

    adj_e = {Specie.tiger: [Specie.grizzly_bear, Specie.horse],
             Specie.polar_bear: [Specie.bengal_tiger],
             Specie.bengal_tiger: [Specie.rabbit],
             Specie.grizzly_bear: [Specie.tiger, Specie.rabbit],
             Specie.rabbit: [], Specie.horse: []}
    eco = Ecosystem(zones, flocks=flocks, adj_z=adj_z, adj_e=adj_e)
    solution = eco.zones
    for item in solution:
        print(f'{item.id} : {[flock.__type__ for flock in item.flocks]}')


if __name__ == "__main__":
    main()
