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


import sys
import xml.etree.ElementTree as ET

from graphviz import Digraph

import xml_generator


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


def xml_to_dot(xml_filename, dot_filename, river):
    tree = ET.parse(xml_filename)
    xml_root = tree.getroot()

    valmatrix_data = extract_data_from_xml(xml_root)

    name = dot_filename.split("/")[-1].split(".")[0]
    dot_graph = Digraph(name)
    nodes = extract_nodes_from_xml(xml_root)

    name_nodes = [keys for keys in nodes.keys()]

    dico_states_de_base = extract_states_de_base(xml_root, nodes)

    # add the base nodes with beautify names in box shape with color
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

    dot_graph.node("initial", shape="box", label=f"{text_initial}", color="green", style="filled")
    dot_graph.node("final", shape="box", label=f"{text_final}", color="red", style="filled")

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
        dot_graph.edge(initial_values_str, final_values_str, arrowhead="open")

    with open(dot_filename, "w") as f:
        f.write(dot_graph.source)


def dot_to_xml(input_filename, output_filename):
    #     convert dot to xml
    with open(input_filename, "r") as f:
        dot_graph = f.readlines()

    # get the name of the graph
    name = dot_graph[0].split(" ")[1].split(";")[0]

    dot_graph = dot_graph[1:-1]
    dot_graph = [line.strip() for line in dot_graph]
    dot_graph = [line for line in dot_graph if line != ""]
    dot_graph = [line for line in dot_graph if line[0] != "#"]

    nodes = []
    edges = []
    for line in dot_graph:
        if line[0] == '"' or "->" in line:
            nodes.append(line)
        else:
            edges.append(line)
    initial_edges = {}
    final_edges = {}

    for node in edges:
        node_type = node.split(" ")[0]
        node_data = node.split("label=")[1].split("\"")[1]
        edges_name = []
        node_value = []
        if river == "true":
            node_part = node_data.split("|")
            G = node_part[0].split(", ")
            D = node_part[1].split(", ")
            G = G[:-1]
            D = D[:-1]
            for part in G:
                if " " in part:
                    edges_name.append(part.split(" ")[1])
                    node_value.append(part.split(" ")[0])
                elif part != "":
                    edges_name.append(part)
                    node_value.append(1)
                elif part == "":
                    edges_name.append(part)
                    node_value.append(0)
            for part in D:
                if " " in part:
                    edges_name.append(part.split(" ")[1])
                    node_value.append(part.split(" ")[0])
                elif part != "":
                    edges_name.append(part)
                    node_value.append(0)
                elif part == "":
                    edges_name.append(part)
                    node_value.append(0)

        else:
            node_part = node_data.split(", ")
            for part in node_part:
                edges_name.append(part.split(" : ")[0])
                node_value.append(part.split(" : ")[1])

        if node_type == "initial":
            for i in range(len(edges_name)):
                initial_edges[f"i{edges_name[i]}"] = node_value[i]
        else:
            for i in range(len(edges_name)):
                if river == "true":
                    final_edges[f"f{edges_name[i]}"] = int(node_value[i])
                else:
                    if node_value[i] == 0:
                        final_edges[f"f{edges_name[i]}"] = int(initial_edges[f"i{edges_name[i]}"])
                    else:
                        final_edges[f"f{edges_name[i]}"] = int(node_value[i])

    #     partie recuperation des data
    if river == "true":

        init_convert = [int(initial_edges[key]) for key in initial_edges.keys()]
        final_convert = [int(final_edges[key]) for key in final_edges.keys()]


    else:

        init_convert = [int(initial_edges[key]) for key in
                        initial_edges.keys()]  # dict_keys(['iL', 'iC', 'iS', 'iB']) dict_keys(['iL', 'iC', 'iS', 'iB', 'i'])
        final_convert = [int(final_edges[key]) for key in final_edges.keys()]

    data = []

    for node in nodes:

        init, final = node.split(" -> ")[0], node.split(" -> ")[1]

        if "initial" in init:

            init = init_convert
        elif "final" in init:

            init = final_convert
        else:
            initG = init.split("|")[0].strip("\"").split(", ")[:-1]
            if river == "true":

                temp_data = [0] * len(edges_name)
                name_pas_use = edges_name.copy()
                for elt in initG:
                    if elt != "":
                        if " " in elt:
                            weight = elt.split(" ")[0]
                            name = elt.split(" ")[1]
                            if name in name_pas_use:
                                temp_data[edges_name.index(name)] = int(weight)
                                name_pas_use.remove(name)
                        else:
                            if elt in name_pas_use:
                                temp_data[edges_name.index(elt)] = 1
                                name_pas_use.remove(elt)

                for manquant in name_pas_use:
                    temp_data[edges_name.index(manquant)] = 0

                init = temp_data
            else:
                init = list(map(int, init.strip("\"").split(", ")))

        if "final" in final:

            final = final_convert
        elif "initial" in final:

            final = init_convert
        else:
            finalG = final.split("|")[0].strip("\"").split(", ")[:-1]

            if river == "true":
                temp_data = [0] * len(edges_name)
                name_pas_use = edges_name.copy()
                for elt in finalG:
                    if elt != "":
                        if " " in elt:
                            weight = elt.split(" ")[0]
                            name = elt.split(" ")[1]
                            if name in name_pas_use:
                                temp_data[edges_name.index(name)] = int(weight)
                                name_pas_use.remove(name)
                        else:
                            if elt in name_pas_use:
                                temp_data[edges_name.index(elt)] = 1
                                name_pas_use.remove(elt)
                for manquant in name_pas_use:
                    temp_data[edges_name.index(manquant)] = 0

                final = temp_data
            else:
                final = list(map(int, final.strip("\"").split(", ")))

        value = " ".join(map(str, init + final))
        data.append(value)

    # de 0 au max de chaque noeud    [5,3,2] , [10,5,3] -> [[0...10],[0...5],[0...3]]
    max_possible = [0 for i in range(len(edges_name))]
    # on doit sortir le max de chaque noeud [5,3,2] , [10,5,3] -> [10,5,3]
    for i in range(len(data)):
        for j in range(len(edges_name)):
            if int(data[i].split(" ")[j]) > max_possible[j]:
                max_possible[j] = int(data[i].split(" ")[j])

    valeur_possible = [[i for i in range(max_possible[j] + 1)] for j in range(len(edges_name))]

    xml_generator.generator(name=output_filename, initial=init_convert, final=final_convert, data=data,
                            node_names=edges_name, possible_value=valeur_possible)


if __name__ == "__main__":
    parametres = sys.argv
    if len(parametres) != 5:
        print("Usage: python3 converter.py -r <river> -type <type [xtd, dtx]> -i <input file> -o <output file>")
        sys.exit(1)

    for i in range(1, len(parametres), 2):
        if parametres[i] == "-r":
            river = parametres[i + 1]
        elif parametres[i] == "-type":
            operation = parametres[i + 1]
        elif parametres[i] == "-i":
            input_filename = parametres[i + 1]
        elif parametres[i] == "-o":
            output_filename = parametres[i + 1]

    print(f"in {input_filename} out {output_filename} type {operation} river {river}")

    if operation == "xtd":
        print("Converting XML to DOT...")
        print(f"Input file: {input_filename}")
        print(f"Output file: {output_filename}")
        print(f"River: {river}")

        xml_to_dot(xml_filename=input_filename, dot_filename=output_filename, river=river)
    elif operation == "dtx":
        print("Converting DOT to XML...")
        print(f"Input file: {input_filename}")
        print(f"Output file: {output_filename}")
        print(f"River: {river}")
        dot_to_xml(input_filename, output_filename)
    else:
        print("Invalid operation. Use 'xtd' or 'dtx'.")
        sys.exit(1)
