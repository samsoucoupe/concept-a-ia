import argparse
import json

import xml_generator as xml_generator


def test_regle(init=[], state=[]):
    state_size = len(state) - 1
    regle_obligatoire = data["info_problem"]["regle_obligatoire"]
    if regle_obligatoire == []:
        return True
    EGALE = False
    SUP = False
    ID_SUP = 0
    for elt in regle_obligatoire:
        if elt == "EGALE":
            EGALE = True
        elif elt == "SUPERIEUR":
            SUP = True
        else:
            if elt.isdigit():
                ID_SUP = int(elt)

    if EGALE and SUP:
        SupG = state[ID_SUP]
        SupD = int(data["element"][str(ID_SUP)]["quantite"].split(",")[1]) - state[ID_SUP]
        for i in range(state_size):
            INFiG = state[i]
            INFiD = int(data["element"][str(i)]["quantite"].split(",")[1]) - state[i]
            if (INFiG > SupG and SupG != 0) or (INFiD > SupD and SupD != 0):
                return False
        return True


    elif EGALE:
        for i in range(state_size):
            for j in range(state_size):
                if i != j:
                    if state[i] != state[j]:
                        return False
        return True

    elif SUP:
        SupG = state[ID_SUP]
        SupD = int(data["element"][str(ID_SUP)]["quantite"].split(",")[1]) - state[ID_SUP]
        for i in range(state_size):
            INFiG = state[i]
            INFiD = int(data["element"][str(i)]["quantite"].split(",")[1]) - state[i]
            if (INFiG >= SupG and SupG != 0) or (INFiD >= SupD and SupD != 0):
                return False
        return True


def test_compatibilite(state=[]):
    for i in range(len(state) - 1):
        for j in imcompatiblité[i]:

            #         si on a au moins de 1 chaque a gauche ou a droite
            if state[i] > 0 and state[j] > 0 and state[-1] == 0:
                return True
            #         idem pour a droite
            if int(data["element"][str(i)]["quantite"].split(",")[1]) - state[i] > 0 and int(
                    data["element"][str(j)]["quantite"].split(",")[1]) - state[j] > 0 and state[-1] == 1:
                return True
    return False


def generate_transition_text(current, new):
    init = " ".join([str(x) for x in current])
    final = " ".join([str(x) for x in new])
    return f"{init} {final}"


def convert_to_xml_list(current, variations):
    xml_list = []
    for i in range(len(variations)):
        temp_txt = generate_transition_text(current, variations[i])
        xml_list.append(f"{temp_txt}")

    return xml_list


def valid_values(state, possible_value, init, actual_transition_list=[]):
    if len(state) == 0 or (generate_transition_text(init, state) in actual_transition_list) or (
            state == init and state != final) or (test_compatibilite(state) and liste_imcomp != []):
        return False
    if not test_regle(init=init, state=state):
        return False
    for i in range(len(state)):
        if state[i] not in possible_value[i]:
            return False

    return True


def generate_variation(state, possible_value, actual_transition_list=[], final=[], init=[], type_probleme="sceau"):
    # pour chaque noeud
    # on peut vider, remplir ou verser
    def vider(i):
        if state[i] != 0:
            new_state = list(state)
            new_state[i] = 0
            return new_state

    def remplir(i):
        if state[i] != possible_value[i][-1]:
            new_state = list(state)
            new_state[i] = possible_value[i][-1]
            return new_state

    def verser(i, j):
        # on transfert de i vers j
        new_state = state.copy()
        if new_state[i] + new_state[j] <= possible_value[j][-1] and new_state[i] != 0:
            new_state[j] += new_state[i]
            new_state[i] = 0
        else:
            new_state[i] -= possible_value[j][-1] - new_state[j]
            new_state[j] = possible_value[j][-1]
        return new_state

    def changer_rive(state, boat_size=boat_size, move_solo=boat_only):

        def all_transition_mais_sans_changer_rive(state=[], poids=1, rive_actuelle=1, state_init=[], max_diff=-1):
            if max_diff != -1:
                for i in range(len(state) - 1):
                    if abs(state_init[i] - state[i]) > max_diff:
                        if verbose:
                            print(f"on cut la branche {state_init} {state}")
                        return []

            if poids < 0:
                if verbose:
                    print("c'est trop louurd")
                return []
            elif poids == 0:
                if verbose:
                    print(f"c'est bon capacities atteinte avec {state}")
                return [state.copy()]

            else:
                variations = [state.copy()]
                if verbose:
                    print(f"on a passser les conditions de base avec {state_init} => {state} {poids} {rive_actuelle}")
                new_state = state.copy()
                for i in range(len(state) - 1):
                    size = float(data["element"][str(i)]["poids"])
                    new_state = state.copy()

                    if rive_actuelle == 1:
                        if state[i] != 0:
                            new_state[i] -= 1
                            variations += all_transition_mais_sans_changer_rive(new_state, poids - size, rive_actuelle,
                                                                                state_init, max_diff)
                            new_state[i] += 1
                    else:
                        if state[i] != possible_value[i][-1]:
                            new_state[i] += 1
                            variations += all_transition_mais_sans_changer_rive(new_state, poids - size, rive_actuelle,
                                                                                state_init, max_diff)
                            new_state[i] -= 1

                return variations

        new_state = state.copy()
        variations = []
        max_diff = -1
        if boat_size == 0:
            return []
        if data["info_problem"]["regle_traverser"] != "":
            if "DC" in data["info_problem"]["regle_traverser"]:
                max_diff = int(data["info_problem"]["regle_traverser"].split(" ")[0])

        if move_solo:
            if state[-1] == 1:
                new_state[-1] = 0
                variations.append(new_state.copy())
                new_state[-1] = 1

            else:
                new_state[-1] = 1
                variations.append(new_state.copy())
                new_state[-1] = 0

        if state[-1] == 1:
            new_state[-1] = 0
            for i in range(len(state) - 1):
                size = data["element"][str(i)]["poids"]
                if state[i] > 0 and size <= boat_size:
                    new_state[i] -= 1
                    new_variations = all_transition_mais_sans_changer_rive(new_state.copy(), boat_size - size,
                                                                           state[-1], state, max_diff)
                    variations.extend(new_variations)
                    new_state[i] += 1
        else:
            new_state[-1] = 1
            for i in range(len(state) - 1):
                size = data["element"][str(i)]["poids"]
                max_quantite = int(data["element"][str(i)]["quantite"].split(",")[1])
                if state[i] < max_quantite and size <= boat_size:
                    new_state[i] += 1
                    new_variations = all_transition_mais_sans_changer_rive(new_state.copy(), boat_size - size,
                                                                           state[-1], state, max_diff)
                    variations.extend(new_variations)
                    new_state[i] -= 1

        return variations

    if state == final:
        new_state = [final]
    else:
        new_state = []
        if type_probleme == "sceau":

            for i in range(len(state)):
                if "vider" in list_function:
                    temp_state = vider(i)
                    if temp_state != None:
                        new_state.append(temp_state.copy())
                if "remplir" in list_function:
                    temp_state = remplir(i)
                    if temp_state != None:
                        new_state.append(temp_state.copy())
                if "transferer" in list_function:
                    for j in range(len(state)):
                        if i != j:
                            temp_state = verser(i, j)

                            if temp_state != None:
                                new_state.append(temp_state.copy())


        elif type_probleme == "river":
            new_thing = changer_rive(state)
            new_state.extend(new_thing)

    #     on va test les nouvelles valeurs
    valid_states = []
    temp_transition_list = actual_transition_list.copy()
    for i in range(len(new_state)):
        if valid_values(state=new_state[i], possible_value=possible_value, init=state,
                        actual_transition_list=temp_transition_list):
            valid_states.append(new_state[i])
            temp_transition_list.append(generate_transition_text(state, new_state[i]))
    if verbose:
        print(f"valid_states {valid_states} de new_state {new_state}")
    return valid_states


def main(initial, final, possible_value, type_probleme="sceau"):
    states = [initial]
    stack = [initial]
    xml_list = []
    while stack != []:
        state = stack.pop()
        new_state = generate_variation(state=state, possible_value=possible_value, actual_transition_list=xml_list,
                                       final=final, init=initial, type_probleme=type_probleme)

        if new_state != []:
            xml_list += convert_to_xml_list(state, new_state)
            states += new_state
            stack += new_state

    return states, xml_list


if __name__ == '__main__':
    # parser
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--rulesfiles', type=str, default="Rules/Rules_LCS.json")
    parser.add_argument('-o', '--output', type=str, default="XML/output.xml")
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()
    rulesfiles = args.rulesfiles
    output = args.output
    verbose = args.verbose
    if verbose:
        print(f"rulesfiles {rulesfiles}")
        print(f"output {output}")
    data = json.load(open(rulesfiles, "r"))

    # {'element': {'0': {'name': 'S12', 'quantite': '0,12', 'incompatible': ''}, '1': {'name': 'S8', 'quantite': '0,8', 'incompatible': ''}, '2': {'name': 'S5', 'quantite': '0,5', 'incompatible': ''}}, 'info_problem': {'type': 'sceau', 'actions_possible': {'vider': 0, 'remplir': 0, 'transferer': 0}, 'position_initial': [12, 0, 0], 'position_final': [6, 6, 0], 'boat_only': 'False', 'boat_size': 1, 'regle_obligatoire': None}}
    initial = data["info_problem"]["position_initial"]
    final = data["info_problem"]["position_final"]
    possible_value = []
    name_nodes = []
    max_boats = []
    for i in range(len(data["element"])):
        name_nodes.append(data["element"][str(i)]["name"])
        q = data["element"][str(i)]["quantite"].split(",")
        min_value = q[0]
        max_value = q[1]
        possible_value.append([x for x in range(int(min_value), int(max_value) + 1)])
        max_boats.append(int(max_value))

    imcompatiblité = {}
    for i in range(len(data["element"])):
        liste_imcomp = data["element"][str(i)]["incompatible"]
        if liste_imcomp != []:
            imcompatiblité[i] = liste_imcomp
        else:
            imcompatiblité[i] = []

    type = data["info_problem"]["type"]

    if type == "river":
        name_nodes.append("B")
        possible_value.append([0, 1])
        regle_traverser = data["info_problem"]["regle_traverser"]

    list_function = []
    for func in data["info_problem"]["actions_possible"]:
        if data["info_problem"]["actions_possible"][func] == 1:
            list_function.append(func)
    boat_only = data["info_problem"]["boat_only"] == "True"
    boat_size = data["info_problem"]["boat_size"]

    states, xml_list = main(initial, final, possible_value, type_probleme=type)
    if verbose:
        print(states)
        print(xml_list)
        print(len(xml_list))

    xml_generator.generator(name=output, initial=initial, final=final, possible_value=possible_value,
                            node_names=name_nodes, data=xml_list)
