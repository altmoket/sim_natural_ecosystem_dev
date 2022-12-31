import sys
from src.components.simulation import Simulator
from src.ecosystems.ecosystem import Ecosystem
from src.components.zone import Zone
from src.components.classes.specie import *
from src.components.flock import Flock
from src.components.utils import Habitat
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

zone1:Zone=Zone(Habitat.Tropical)
zone2:Zone=Zone(Habitat.Tempered)
zone3:Zone=Zone(Habitat.Tropical)
flock1:Flock=Flock('horse',zone1,34,13)
flock2:Flock=Flock('tiger',zone1,34,13)
flock3:Flock=Flock('horse',zone2,32,45)
flock4:Flock=Flock('horse',zone3,21,14)
flock5:Flock=Flock('horse',zone3,12,23)
zone1.add_flock(flock1)
zone1.add_flock(flock2)
zone2.add_flock(flock3)
zone3.add_flock(flock4)
zone3.add_flock(flock5)
eco=Ecosystem([zone1,zone2,zone3])
sim=Simulator(eco,15)
sim.simulate()