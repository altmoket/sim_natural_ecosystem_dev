import sys
from scripts.generate.specie import generate_specie
from scripts.consult.help import show_help

action_dictionary = {
    'generate': generate_specie,
    '--help': show_help
}

def dispatcher(action, dictionary):
    try:
        return dictionary[action]
    except:
        return None

def main():
    args = sys.argv
    len_args = len(args)
    if len_args == 1:
        fun = dispatcher('--help', action_dictionary)
        assert fun is not None
        fun()
        return
    if len_args == 2:
        action = args[1]
        fun = dispatcher(action, action_dictionary)
        assert fun is not None
        fun()
        return
    if len_args == 4:
        action, element, name = args[1],args[2],args[3]
        fun = dispatcher(action, action_dictionary)
        assert fun is not None
        if element == 'specie':
            fun(name)

if __name__ == "__main__":
    main()
