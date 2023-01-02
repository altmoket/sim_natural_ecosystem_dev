from src import * 

# PARA FACILIDAD EN LA SIMULACION GENERANDO ZONAS, MANADAS 
# Y UBICANDOLAS SATISFACTORIAMENTE EN ZONAS SEGUN CSP
def main():
    zone1 = Zone(Habitat.tropical)
    zone2 = Zone(Habitat.tempered)
    zone3 = Zone(Habitat.tropical)
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
    eco=Ecosystem([zone1,zone2,zone3])
    sim=Simulator(eco,15)
    sim.simulate()

    print('CSP')
    flock1 = Flock(Specie.bengal_tiger)
    flock2 = Flock(Specie.grizzly_bear)
    flock3 = Flock(Specie.rabbit)
    flock4 = Flock(Specie.tiger)
    flock5 = Flock(Specie.polar_bear)
    flock6 = Flock(Specie.bengal_tiger)
    flock7 = Flock(Specie.horse)
    flocks =[flock1,flock2,flock3,flock4,flock5,flock6,flock7]

    zone1 = Zone(Habitat.tempered)
    zone2 = Zone(Habitat.desertic)
    zone4 = Zone(Habitat.tropical)
    zone3 = Zone(Habitat.polar)
    zones = [zone1,zone2,zone3,zone4]

    adj_z={zone1:[zone2],zone2:[zone1,zone3],zone3:[zone2,zone4],zone4:[zone3]}

    adj_e={
    Specie.tiger:[Specie.grizzly_bear,Specie.horse],
    Specie.polar_bear:[Specie.bengal_tiger],
    Specie.bengal_tiger:[Specie.rabbit],
    Specie.grizzly_bear:[Specie.tiger,Specie.rabbit],
    Specie.rabbit:[], Specie.horse:[]}

    solution = CSP(flocks,zones,adj_z,adj_e)
    for item in solution.items():
        print(f'{item[0].__type__} : {item[1].type}')



if __name__ == "__main__":
    main()