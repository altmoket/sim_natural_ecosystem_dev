from src import *
#from scripts.generate.specie import generate_specie
#from scripts.consult.help import show_help

#action_dictionary = {
#    'generate': generate_specie,
#    '--help': show_help
#}

#def dispatcher(action, dictionary):
#    try:
#        return dictionary[action]
#    except:
#        return None

#def main():
#    args = sys.argv
#    len_args = len(args)
#    if len_args == 1:
#        fun = dispatcher('--help', action_dictionary)
#        assert fun is not None
#        fun()
#       return
#   if len_args == 2:
#        action = args[1]
#        fun = dispatcher(action, action_dictionary)
#        assert fun is not None
#        fun()
#        return
#    if len_args == 4:
#        action, element, name = args[1],args[2],args[3]
#        fun = dispatcher(action, action_dictionary)
#        assert fun is not None
#        if element == 'specie':
#            fun(name)

# if __name__ == "__main__":
#    main()

# PARA FACILIDAD EN LA SIMULACION GENERANDO ZONAS, MANADAS 
# Y UBICANDOLAS SATISFACTORIAMENTE EN ZONAS SEGUN CSP
zone1 = Zone(Habitat.Tropical)
zone2 = Zone(Habitat.Tempered)
zone3 = Zone(Habitat.Tropical)
flock1 = Flock('horse', 34, 13)
flock2 = Flock('tiger', 34, 13)
flock3 = Flock('bear' , 32, 45)
flock4 = Flock('horse', 21, 14)
flock5 = Flock('horse', 12, 23)
flock1.asign_zone(zone1)
flock2.asign_zone(zone1)
flock3.asign_zone(zone2)
flock4.asign_zone(zone3)
flock5.asign_zone(zone3)
eco=Ecosystem([zone1,zone2,zone3])
sim=Simulator(eco,15)
sim.simulate()