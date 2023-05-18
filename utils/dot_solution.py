#  Copyright (c) 2023. Samy Ben dhiab All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#   #
#         http://www.apache.org/licenses/LICENSE-2.0
#   #
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#   #
#         http://www.apache.org/licenses/LICENSE-2.0
#   #
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import sys
import xml.etree.ElementTree as ET

from graphviz import Digraph


def extract_data_from_xml(xml_root):
    valmatrix_data = [
        list(map(int, data.text.split()))
        for data in xml_root.find("values").find("valmatrix").findall("data")
    ]

    return valmatrix_data


def extract_nodes_from_xml(xml_root):
    # get id  and all possible values of each node
    list_of_nodes = [
        list(map(int, data.text.split()))
        for data in xml_root.find("variables").findall("var[@type='int extensional']")
    ]
    dico_data = {}
    nodes = xml_root.find('variables').findall('var[@type="int extensional"]')
    for node in nodes:
        dico_data[node.attrib['id']] = list_of_nodes[nodes.index(node)]
    return dico_data


def extract_states_de_base(xml_root, nodes):
    # return dico

    initial_nodes = [f"i{node}" for node in nodes]
    final_nodes = [f"f{node}" for node in nodes]
    dico_states_de_base = {"initial": [], "final": []}
    # recupere toutes les variables avec comme id un des elements initial_nodes ou final_nodes
    # get the initial and final nodes names
    for elt in initial_nodes:
        dico_states_de_base["initial"].append(int(xml_root.find("variables").find(f"var[@id='{elt}']").text))
    for elt in final_nodes:
        dico_states_de_base["final"].append(int(xml_root.find("variables").find(f"var[@id='{elt}']").text))

    return dico_states_de_base


def xml_to_dot(xml_filename, dot_filename, solutions, river):
    tree = ET.parse(xml_filename)
    xml_root = tree.getroot()

    valmatrix_data = extract_data_from_xml(xml_root)

    name = dot_filename.split("/")[-1].split(".")[0]

    nodes = extract_nodes_from_xml(xml_root)

    name_nodes = [keys for keys in nodes.keys()]

    dico_states_de_base = extract_states_de_base(xml_root, nodes)

    if river != "true":
        text_initial = [f"{name_nodes[i]} : {nodes[name_nodes[i]][dico_states_de_base['initial'][i]]}" for i in
                        range(len(name_nodes))]
        text_initial = ", ".join(map(str, text_initial))
        text_final = [f"{name_nodes[i]} : {nodes[name_nodes[i]][dico_states_de_base['final'][i]]}" for i in
                      range(len(name_nodes))]
        text_final = ", ".join(map(str, text_final))

    else:
        text_initial_g = ""
        text_initial_d = ""
        text_final_g = ""
        text_final_d = ""
        for i in range(len(name_nodes)):
            keys = name_nodes[i]
            value_node_i = nodes[keys][dico_states_de_base['initial'][i]]
            value_node_f = nodes[keys][dico_states_de_base['final'][i]]
            valeur = nodes[keys][dico_states_de_base['initial'][i]]

            if value_node_i > 0:
                text_initial_g += f"{value_node_i} {keys}, "
                if valeur > value_node_i:
                    valeur = valeur - value_node_i
                    text_initial_d += f"{valeur} {keys}, "
            else:
                if valeur == 1:
                    text_initial_d += f"{keys}, "
                else:
                    text_initial_d += f"{valeur} {keys}, "

            if value_node_f > 0:
                text_final_g += f"{value_node_f} {keys}, "
                if valeur > value_node_f:
                    valeur = valeur - value_node_f
                    text_final_d += f"{valeur} {keys}, "
            else:
                if valeur == 1:
                    text_final_d += f"{keys}, "
                else:
                    text_final_d += f"{valeur} {keys}, "

        text_initial = f"{text_initial_g}|{text_initial_d}"
        text_final = f"{text_final_g}|{text_final_d}"

    for num in range(len(solutions)):
        dot_graph = Digraph(name)
        dot_graph.concentrate = True
        dot_graph.node("initial", shape="box", label=f"{text_initial}", color="green", style="filled")
        dot_graph.node("final", shape="box", label=f"{text_final}", color="red", style="filled")
        solution = solutions[num]

        for transition in valmatrix_data:
            initial_values = transition[:len(nodes)]
            final_values = transition[len(nodes):]
            if river == "true":

                # prendre la valeurs et si elle est differentes de 1 on affiche le nombre + l'id du noeud sinon on affiche l'id du noeud

                if initial_values == dico_states_de_base["initial"]:
                    initial_values_str = "initial"
                elif initial_values == dico_states_de_base["final"]:
                    initial_values_str = "final"
                else:
                    initial_values_g = ""
                    initial_values_d = ""
                    for i in range(len(nodes)):
                        keys = name_nodes[i]
                        value_node_i = initial_values[i]
                        valeur = nodes[keys][dico_states_de_base['initial'][i]]
                        if value_node_i > 0:
                            initial_values_g += f"{value_node_i} {keys}, "
                            if valeur > value_node_i:
                                valeur = valeur - value_node_i
                                initial_values_d += f"{valeur} {keys}, "
                        else:
                            if valeur == 1:
                                initial_values_d += f"{keys}, "
                            else:
                                initial_values_d += f"{valeur} {keys}, "
                    initial_values_str = f"{initial_values_g}|{initial_values_d}"

                if final_values == dico_states_de_base["final"]:
                    final_values_str = "final"
                elif final_values == dico_states_de_base["initial"]:
                    final_values_str = "initial"
                else:
                    final_values_g = ""
                    final_values_d = ""
                    for i in range(len(nodes)):
                        keys = name_nodes[i]
                        valeur = nodes[keys][dico_states_de_base['initial'][i]]
                        value_node_f = final_values[i]
                        if value_node_f > 0:
                            final_values_g += f"{value_node_f} {keys}, "
                            if valeur > value_node_f:
                                valeur = valeur - value_node_f
                                final_values_d += f"{valeur} {keys}, "
                        else:
                            if valeur == 1:
                                final_values_d += f"{keys}, "
                            else:
                                final_values_d += f"{valeur} {keys}, "

                    final_values_str = f"{final_values_g}|{final_values_d}"
            else:
                if initial_values == dico_states_de_base["initial"]:
                    initial_values_str = "initial"
                elif initial_values == dico_states_de_base["final"]:
                    initial_values_str = "final"
                else:
                    initial_values_str = ", ".join(map(str, initial_values))
                if final_values == dico_states_de_base["initial"]:
                    final_values_str = "initial"
                elif final_values == dico_states_de_base["final"]:
                    final_values_str = "final"
                else:
                    final_values_str = ", ".join(map(str, final_values))
            trouve = False
            for i in range(len(solution) - 1):
                if solution[i] == initial_values and solution[i + 1] == final_values:
                    # mettre en gras le lien
                    trouve = True
            if trouve:
                dot_graph.edge(initial_values_str, final_values_str, penwidth="3", arrowhead="open")
            else:
                dot_graph.edge(initial_values_str, final_values_str, arrowhead="open")

        with open(dot_filename + str(num + 1) + ".dot", "w") as f:
            f.write(dot_graph.source)


def extract_solution(file_name="test.txt"):
    file = open("TXT/" + file_name, "r")
    lines = file.readlines()
    file.close()
    while not lines[0].startswith("Number of Solutions:"):
        lines.pop(0)
    lines.pop(0)
    names = []
    data = lines[0].split("(")[1].split(")")[0].split(" ")[0:-1]

    for elt in data:
        nom = elt.split("=")[0]
        names.append(nom)

    solution = []
    for lignes in lines:
        data = lignes.replace(")", ",").replace("(", "").split(",")[0:-1]
        temp_solution = []
        for elt in data:
            temp = [0 for i in range(len(names))]
            temp_data = elt.split(" ")[0:-1]
            for i in range(len(names)):
                temp[i] = int(temp_data[i].split("=")[1])
            temp_solution.append(temp)

        solution.append(temp_solution)
    return solution


if __name__ == "__main__":
    print(sys.argv)
    name = sys.argv[1]
    river = sys.argv[2]
    input_filename = f"XML/{name}.xml"
    output_filename = f"DOT/{name}/{name}_Sol_"

    data = extract_solution(name + ".txt")
    xml_to_dot(xml_filename=input_filename, dot_filename=output_filename, solutions=data, river=river)
