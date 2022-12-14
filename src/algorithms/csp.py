from ..components import *
from collections import defaultdict
import random

def CSP(flocks: list[Flock], zones: list[Zone], adj_z: dict[Zone, list[Zone]], adj_e: dict[Specie, list[Specie]]):
    options:dict[Flock,list[Zone]] = {}
    arcs: list[(Flock, Flock)] = []
    assigments: dict[Flock, Zone] = defaultdict(lambda: None)
    non_assigned: list[Flock] = flocks.copy()
    adj_f: dict[Flock, list[Flock]] = defaultdict(lambda: [])
    # Determinar opciones para cada una de las variables
    for flock in flocks:
        options[flock] = list(filter(lambda zone: zone.type in Species.search_specie_type(
            flock.__type__).habitat(), zones))
        if len(options[flock]) == 0:
            options[flock]=zones.copy()
        if len(options[flock]) == 1:
            assigments[flock] = options[flock][0]
            non_assigned.remove(flock)
    # Determinar arcos de restricciones
    for i in range(len(flocks)):
        for j in range(i+1, len(flocks)):
            flock1 = flocks[i]
            flock2 = flocks[j]
            if flock2.__type__ in adj_e[flock1.__type__]:
                adj_f[flock1].append(flock2)
                arcs.append((flock1, flock2))
            if flock1.__type__ in adj_e[flock2.__type__]:
                adj_f[flock2].append(flock1)
                arcs.append((flock2, flock1))

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
    for flock in non_assigned:
        valid_zones=list(filter(lambda zone : not zone in assigments.values(),temp_options[flock]))
        n_options=len(valid_zones)
        if n_options == 0:
            n_options=len(temp_options[flock])
            valid_zones=temp_options[flock]
        index=random.randint(0,n_options-1)
        assigments[flock] = valid_zones[index]
    return assigments


def Backtrack_Search(options: dict[Flock, list[Zone]], assigment: dict[Flock, Zone], non_assigned: list[Flock], arcs: list[(Flock, Flock)], adj_z: dict[Zone, list[Zone]], adj_f: dict[Flock, list[Flock]]):
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
            for flock in adj_f[current_arc[0]]:
                arcs.append((flock, current_arc[0]))
    # Asignar una variable
    current = non_assigned[0]
    for value in options[current]:
        # comprobar consistencia con los valores anteriores (Falta comprobar los q pueden atacar al nuevo grupo)
        valid_value = True
        for flock in assigment.items():
            if (flock[1] == value or flock[1] in adj_z[value]) and (current in adj_f[flock[0]] or flock[0] in adj_f[current]):
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