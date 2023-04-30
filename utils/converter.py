import sys
import xml.etree.ElementTree as ET
from graphviz import Digraph, Source


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
    if river != "True":
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

            if value_node_i > 1:
                text_initial_g += f"{value_node_i} {keys}, "
                if valeur > value_node_i:
                    valeur = valeur - value_node_i
                    text_initial_d += f"{valeur} {keys}, "
            elif value_node_i == 1:
                text_initial_g += f"{keys}, "
                if valeur > value_node_i:
                    valeur = valeur - value_node_i
                    text_initial_d += f"{valeur} {keys}, "
            else:
                if valeur==1 :
                    text_initial_d += f"{keys}, "
                else:
                    text_initial_d += f"{valeur} {keys}, "

            if value_node_f > 1:
                text_final_g += f"{value_node_f} {keys}, "
                if valeur > value_node_f:
                    valeur = valeur - value_node_f
                    text_final_d += f"{valeur} {keys}, "
            elif value_node_f == 1:
                text_final_g += f"{keys}, "
                if valeur > value_node_f:
                    valeur = valeur - value_node_f
                    text_final_d += f"{valeur} {keys}, "
            else:
                if valeur==1 :
                    text_final_d += f"{keys}, "
                else:
                    text_final_d += f"{valeur} {keys}, "

        text_initial_g = text_initial_g[:-2]
        text_initial_d = text_initial_d[:-2]
        text_final_g = text_final_g[:-2]
        text_final_d = text_final_d[:-2]
        text_initial = f"{text_initial_g} | {text_initial_d}"
        text_final = f"{text_final_g} | {text_final_d}"


    # TODO: ameliorer l'affichage des noeuds de base
    dot_graph.node("initial", shape="box", color="green", label=f"{text_initial}")
    dot_graph.node("final", shape="box", color="red", label=f"{text_final}")

    for transition in valmatrix_data:
        initial_values = transition[:len(nodes)]
        final_values = transition[len(nodes):]

        if river == "True":

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
                    if value_node_i > 1:
                        initial_values_g += f"{value_node_i} {keys}, "
                        if valeur > value_node_i:
                            valeur = valeur - value_node_i
                            initial_values_d += f"{valeur} {keys}, "
                    elif value_node_i == 1:
                        initial_values_g += f"{keys}, "
                        if valeur > value_node_i:
                            valeur = valeur - value_node_i
                            initial_values_d += f"{valeur} {keys}, "
                    else:
                        if valeur==1:
                            initial_values_d += f"{keys}, "
                        else:
                            initial_values_d += f"{valeur} {keys}, "

                initial_values_g = initial_values_g[:-2]
                initial_values_d = initial_values_d[:-2]
                initial_values_str = f"{initial_values_g} | {initial_values_d}"

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
                    if value_node_f > 1:
                        final_values_g += f"{value_node_f} {keys}, "
                        if valeur > value_node_f:
                            valeur = valeur - value_node_f
                            final_values_d += f"{valeur} {keys}, "
                    elif value_node_f == 1:
                        final_values_g += f"{keys}, "
                        if valeur > value_node_f:
                            valeur = valeur - value_node_f
                            final_values_d += f"{valeur} {keys}, "
                    else:
                        if valeur != 1:
                            final_values_d += f"{valeur} {keys}, "
                        else:
                            final_values_d += f"{keys}, "


                final_values_g = final_values_g[:-2]
                final_values_d = final_values_d[:-2]
                final_values_str = f"{final_values_g} | {final_values_d}"

            dot_graph.edge(initial_values_str, final_values_str)

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
            dot_graph.edge(initial_values_str, final_values_str)

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
        if river == "True":
            node_part = node_data.split("|")
            G = node_part[0].split(", ")
            D = node_part[1].split(", ")

            for part in G:
                if " " in part:
                    edges_name.append(part.split(" ")[1])
                    node_value.append(part.split(" ")[0])
                elif part != "":
                    edges_name.append(part)
                    node_value.append(1)

            for part in D:
                if " " in part:
                    edges_name.append(part.split(" ")[1])
                    node_value.append(part.split(" ")[0])
                elif part != "":
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
                final_edges[f"f{edges_name[i]}"] = node_value[i]

    #     partie recuperation des data
    if river == "True":

        init_convert = [int(initial_edges[key]) for key in initial_edges.keys() if initial_edges[key] != ""]
        final_convert = [int(final_edges[key]) for key in final_edges.keys() if final_edges[key] != ""]
    else:
        init_convert = [int(initial_edges[key]) for key in initial_edges.keys()]#dict_keys(['iL', 'iC', 'iS', 'iB']) dict_keys(['iL', 'iC', 'iS', 'iB', 'i'])
        final_convert = [int(final_edges[key]) for key in final_edges.keys()]

    data = []

    for node in nodes:
        init, final = node.split(" -> ")[0], node.split(" -> ")[1]

        if "initial" in init:
            init = init_convert
        elif "final" in init:
            init = final_convert
        else:
            if river == "True":
                temp_data = [0] * len(edges_name)
                I = init.split(" | ")[0].strip("\"").split(", ")

                for i, edge_name in enumerate(edges_name):
                    if edge_name in I:
                        weight = I[I.index(edge_name)].split(" ")[0]
                        temp_data[i] = int(weight) if weight.isdigit() else 1

                init = temp_data
            else:
                init = list(map(int, init.strip("\"").split(", ")))

        if "final" in final:
            final = final_convert
        elif "initial" in final:
            final = init_convert
        else:
            if river == "True":
                temp_data = [0] * len(edges_name)
                F = final.split(" | ")[0].strip("\"").split(", ")

                for i, edge_name in enumerate(edges_name):
                    if edge_name in F:
                        weight = F[F.index(edge_name)].split(" ")[0]
                        temp_data[i] = int(weight) if weight.isdigit() else 1

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

    #     ecriture du fichier xml
    root = ET.Element("root")
    # Créer la racine du document XML
    root = ET.Element("instance", format="Talos")

    # Ajouter les valeurs du document
    values = ET.SubElement(root, "values")

    valmatrix = ET.SubElement(values, "valmatrix", id="transitions")

    for row in data:
        ET.SubElement(valmatrix, "data").text = row

    # Ajouter les variables du document
    variables = ET.SubElement(root, "variables")

    for name in initial_edges:
        var = ET.SubElement(variables, "var", id=f"{name}")
        var.text = str(initial_edges[name])

    for name in final_edges:
        var = ET.SubElement(variables, "var", id=f"{name}")
        var.text = str(final_edges[name])

    for i in range(len(edges_name)):
        name = edges_name[i]
        var = ET.SubElement(variables, "var", id=f"{name}", type="int extensional")
        possible = " ".join(map(str, valeur_possible[i]))
        var.text = possible

    # Ajouter les variables du document
    variables = ET.SubElement(root, "variables")

    vararray = ET.SubElement(variables, "vararray", id="state")
    vararray.text = str(" ".join(map(str, edges_name)))

    vararray = ET.SubElement(variables, "vararray", id="initial")
    vararray.text = str(" ".join(map(str, [x for x in initial_edges.keys()])))

    vararray = ET.SubElement(variables, "vararray", id="final")
    vararray.text = str(" ".join(map(str, [x for x in final_edges.keys()])))

    tree = ET.ElementTree(root)
    tree.write(output_filename, encoding="utf-8", xml_declaration=True)

    with open(output_filename, "r") as f:
        lines = f.readlines()

    with open(output_filename, "w") as f:
        for ligne in lines:
            if ligne.startswith("<?xml"):
                ligne = ligne.replace("?>", " standalone=\"no\"?>")
                f.write(ligne + "\n")
            else:
                f.write(ligne + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 9:
        print("Usage: python3 converter.py -r [True/False] -type [xtd/dtx] -input [input file] -output [output file]")
        sys.exit(1)

    river = None
    operation = None
    input_filename = None
    output_filename = None

    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "-r":
            river = sys.argv[i + 1]
        elif sys.argv[i] == "-type":
            operation = sys.argv[i + 1]
        elif sys.argv[i] == "-input":
            input_filename = sys.argv[i + 1]
        elif sys.argv[i] == "-output":
            output_filename = sys.argv[i + 1]
        else:
            print("Invalid argument. Use -r, -type, -input, -output.")
            sys.exit(1)
    print(f"in {input_filename} out {output_filename} type {operation} river {river}")
    if operation == "xtd":
        print("Converting XML to DOT...")
        print(f"Input file: {input_filename}")
        print(f"Output file: {output_filename}")
        print(f"River: {river}")

        xml_to_dot(xml_filename=input_filename, dot_filename=output_filename, river=river)
    elif operation == "dtx":
        dot_to_xml(input_filename, output_filename)
    else:
        print("Invalid operation. Use 'xtd' or 'dtx'.")
        sys.exit(1)
