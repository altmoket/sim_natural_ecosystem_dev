from ..components import Species,Zone,Specie
from collections import defaultdict
import random

def CSP(animals: list[Species], zones: list[Zone], adj_z: dict[Zone, list[Zone]], adj_e: dict[Specie, list[Specie]]):
    options:dict[Species,list[Zone]] = {}
    arcs: list[(Species, Species)] = []
    assigments: dict[Species, Zone] = defaultdict(lambda: None)
    non_assigned: list[Species] = animals.copy()
    adj_f: dict[Species, list[Species]] = defaultdict(lambda: [])
    # Determinar opciones para cada una de las variables
    for animal in animals:
        options[animal] = list(filter(lambda zone: zone.type in animal.habitat(), zones))
        if len(options[animal]) == 0:
            options[animal]=zones.copy()
        if len(options[animal]) == 1:
            assigments[animal] = options[animal][0]
            non_assigned.remove(animal)
    # Determinar arcos de restricciones
    for i in range(len(animals)):
        for j in range(i+1, len(animals)):
            animal1 = animals[i]
            animal2 = animals[j]
            if animal2._type in adj_e[animal1._type]:
                adj_f[animal1].append(animal2)
                arcs.append((animal1, animal2))
            if animal1._type in adj_e[animal2._type]:
                adj_f[animal2].append(animal1)
                arcs.append((animal2, animal1))

    #creando una copia de las opciones por cada grupo
    temp_options={}
    for item in options.items():
        temp_options[item[0]] = options[item[0]].copy()

    #intentar encontrar una distribucion que satisfaga todas las restricciones
    solution = Backtrack_Search(options, assigments.copy(), non_assigned.copy(), arcs, adj_z, adj_f)
    if solution:
        print("\nValid Distribution") 
        return solution

    # en caso de que no se encuentre una distribucion ideal se le asigna a cada grupo alguna de las zonas en las que puede habitar
    for animal in non_assigned:
        valid_zones=list(filter(lambda zone : not zone in assigments.values(),temp_options[animal]))
        n_options=len(valid_zones)
        if n_options == 0:
            n_options=len(temp_options[animal])
            valid_zones=temp_options[animal]
        index=random.randint(0,n_options-1)
        assigments[animal] = valid_zones[index]
    return assigments


def Backtrack_Search(options: dict[Species, list[Zone]], assigment: dict[Species, Zone], non_assigned: list[Species], arcs: list[(Species, Species)], adj_z: dict[Zone, list[Zone]], adj_f: dict[Species, list[Species]]):
    if len(non_assigned) == 0:
        return assigment
    # comprobando consistencia de los arcos
    while len(arcs) > 0:
        current_arc = arcs.pop(0)
        removed = False
        consistent = False
        for area1 in options[current_arc[0]]:
            for area2 in options[current_arc[1]]:
                if not area1 == area2 and not (area2 in adj_z[area1]):
                    consistent = True
                    break
            if not consistent:
                options[current_arc[0]].remove(area1)
                removed = True
        if removed:
            for animal in adj_f[current_arc[0]]:
                arcs.append((animal, current_arc[0]))
    # Asignar una variable
    current = non_assigned[0]
    for value in options[current]:
        # comprobar consistencia con los valores anteriores (Falta comprobar los q pueden atacar al nuevo grupo)
        valid_value = True
        for animal in assigment.items():
            if (animal[1] == value or animal[1] in adj_z[value]) and (current in adj_f[animal[0]] or animal[0] in adj_f[current]):
                valid_value = False
                break
        if valid_value:
            # llamado recursivo
            assigment[current] = value
            non_assigned.pop(0)
            temp = list(
                filter(lambda arc: not arc[0] == current and not arc[1] == current, arcs))
            recursive_call = Backtrack_Search(
                options, assigment, non_assigned, temp, adj_z, adj_f)
            if recursive_call != None:
                return recursive_call
            non_assigned.insert(0, current)
    return None