#
#  Copyright (c) 2023. Samy Ben Dhiab (Samsoucoupe) All rights reserved.
#  #
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#  #
#        http://www.apache.org/licenses/LICENSE-2.0
#  #
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

import argparse
import json
import os


def init_element_list(type_de_probleme, nb_element, boat, boat_size):
    actions = {"vider": 0, "remplir": 0, "transferer": 0}
    element = {}
    info_problem = {"type": type_de_probleme,
                    "actions_possible": actions,
                    "position_initial": [],
                    "position_final": [],
                    "boat_only": boat,
                    "boat_size": boat_size,
                    "solution_max": 10,
                    "regle_obligatoire": [],
                    "regle_traverser": ""
                    }
    return {"element": element, "info_problem": info_problem}


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="name of the file to create")
args = parser.parse_args()
nom_fichier = args.file or "test"
nom_fichier = "Rules_" + nom_fichier

pwd = os.getcwd()
# folder = "Talos/java"
# java_index = pwd.find(folder)
# actual_folder = pwd[:java_index + len(folder)]
pwd = pwd + "/"
pwd = os.path.join(pwd, "Rules")
separateur = "----------------------------"
actions = {"vider": 0, "remplir": 0, "transferer": 0}

type_de_probleme = input("type de probleme: [sceau, river] ")
while type_de_probleme not in ["sceau", "river"]:
    type_de_probleme = input("type de probleme: [sceau, river] ")

if type_de_probleme == "river":
    boat = input("Bateau peut move solo ? (oui ou non) ")
    while boat not in ["oui", "non"]:
        boat = input("Bateau peut moove solo ? (oui ou non) ")
    boat = boat == "oui"
    boat = str(boat)
else:
    boat = "non"

boat_size = 1

print(separateur)

nb_element = input("Nombre de sceau: " if type_de_probleme == "sceau" else "Nombre d'element distinct: ")
while not nb_element.isdigit():
    nb_element = input("Nombre de sceau: " if type_de_probleme == "sceau" else "Nombre d'element distinct: ")

nb_element = int(nb_element)
liste_element = init_element_list(type_de_probleme, nb_element, boat, boat_size)
print(separateur)

nb_version = 1
for i in range(nb_element):
    if type_de_probleme == "sceau":
        print(f"Sceau {i + 1} - ")
        taille_sceau = input("Quantité max du sceau en L: ")
        while not taille_sceau.isdigit():
            taille_sceau = input("Quantité max du sceau en L: ")
        name = f"S{taille_sceau}"
        liste_name_use = [liste_element["element"][elt]["name"] for elt in liste_element["element"]]
        while name in liste_name_use:
            name = f"S{taille_sceau} ({nb_version})"
            nb_version += 1
        min_value = 0
        max_value = taille_sceau
        quantite = f"{min_value},{max_value}"
        liste_element["element"][i] = {"name": name, "quantite": quantite, "incompatible": ""}

    elif type_de_probleme == "river":
        print(f"Element {i + 1}")
        name = input("nom : ")
        liste_name_use = [liste_element["element"][elt]["name"] for elt in liste_element["element"]]
        while name in liste_name_use:
            name = f"{name} ({nb_version})"
            nb_version += 1
        valeur_min = input("valeur min : ")
        while not valeur_min.isdigit():
            valeur_min = input("valeur min : ")
        valeur_max = input("valeur max : ")
        while not valeur_max.isdigit():
            valeur_max = input("valeur max : ")
        quantite = f"{valeur_min},{valeur_max}"
        poids = input("Combien peuvent etre transporter par le bateau ? ")
        while not poids.isdigit():
            poids = input("Combien peuvent etre transporter par le bateau ? ")
        poids = 1 / int(poids)
        liste_element["element"][i] = {"name": name, "quantite": quantite, "incompatible": "", "poids": poids}

print(separateur)

for i in range(nb_element):
    position_initial = input(f"Position initiale de {liste_element['element'][i]['name']}: ")
    liste_element['info_problem']['position_initial'].append(position_initial)

    position_final = input(f"Position finale de {liste_element['element'][i]['name']}: ")
    liste_element['info_problem']['position_final'].append(position_final)

if type_de_probleme == "river":
    liste_element['info_problem']['position_initial'] = [int(elt) for elt in
                                                         liste_element['info_problem']['position_initial']] + [1]
    liste_element['info_problem']['position_final'] = [int(elt) for elt in
                                                       liste_element['info_problem']['position_final']] + [0]
print(separateur)

B_regles = input("Y a t'il des regles a ajouter ? (oui ou non) ")
while B_regles not in ["oui", "non"]:
    B_regles = input("Y a t'il des regles a ajouter ? (oui ou non) ")
B_regles = B_regles == "oui"

if B_regles and type_de_probleme == "sceau":
    vider = input("Vider un sceau ? (oui ou non) ")
    while vider not in ["oui", "non"]:
        vider = input("Vider un sceau ? (oui ou non) ")
    vider = vider == "oui"
    if vider:
        liste_element["info_problem"]["actions_possible"]["vider"] = 1

    remplir = input("Remplir un sceau ? (oui ou non) ")
    while remplir not in ["oui", "non"]:
        remplir = input("Remplir un sceau ? (oui ou non) ")
    remplir = remplir == "oui"
    if remplir:
        liste_element["info_problem"]["actions_possible"]["remplir"] = 1

    transferer = input("Transferer d'un sceau a un autre ? (oui ou non) ")
    while transferer not in ["oui", "non"]:
        transferer = input("Transferer d'un sceau a un autre ? (oui ou non) ")
    transferer = transferer == "oui"
    if transferer:
        liste_element["info_problem"]["actions_possible"]["transferer"] = 1

    print(separateur)

if B_regles and type_de_probleme == "river":
    print("Les participants doivent-ils être en nombre égal, supérieur ou aucun des deux ?")
    regles = input("0 : égal, 1 : supérieur, 2: supérieur ou égal, 3 : aucun ")
    while regles not in ["0", "1", "2", "3"]:
        regles = input("0 : égal, 1 : supérieur, 2: supérieur ou égal, 3 : aucun ")

    if regles in ["1", "2"]:
        print("Liste des participants :")
        for i in range(nb_element):
            print(f"{i} : {liste_element['element'][i]['name']}")
        id_sup = input("Quel est l'ID de l'élément supérieur ? (Exemple: 1: LOUP 2: CHEVRE 3: SALADE => 1) ")
        while not id_sup.isdigit() or int(id_sup) > nb_element:
            id_sup = input("Quel est l'ID de l'élément supérieur ? (Exemple: 1: LOUP 2: CHEVRE 3: SALADE => 1) ")

    if regles == "0" or regles == "2":
        liste_element["info_problem"]["regle_obligatoire"].append("EGALE")
    if regles == "1" or regles == "2":
        liste_element["info_problem"]["regle_obligatoire"].append("SUPERIEUR")
        liste_element["info_problem"]["regle_obligatoire"].append(id_sup)

    print(separateur)

    print(
        "Voulez-vous limiter le nombre de chaque élément qui se déplace sur le bateau ? (Exemple : 1 de chaque élément maximum) ")
    regles = input("0 : oui, 1 : non ")
    while regles not in ["0", "1"]:
        regles = input("0 : oui, 1 : non ")
    if regles == "0":
        nombre = input("Combien d'éléments maximum ? ")
        while not nombre.isdigit() and nombre != "0":
            nombre = input("Combien d'éléments maximum ? ")
        liste_element["info_problem"]["regle_traverser"] = nombre + "DC"

    print(separateur)

if not B_regles:
    liste_element["info_problem"]["regle_obligatoire"] = []
    liste_element["info_problem"]["regle_traverser"] = ""
    liste_element["info_problem"]["actions_possible"] = {"vider": 1, "remplir": 1, "transferer": 1}

max_solution = input("Combien de coups maximum pour la solution ? ")
while not max_solution.isdigit():
    max_solution = input("Combien de coups maximum pour la solution ? ")
liste_element["info_problem"]["max_solution"] = int(max_solution)

# Ecriture du fichier json
with open(f"{pwd}/{nom_fichier}.json", "w") as f:
    json.dump(liste_element, f, indent=4)
