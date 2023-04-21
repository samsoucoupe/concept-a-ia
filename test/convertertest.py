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
    print(nodes)
    print("nodes ^")

    name_nodes = [keys for keys in nodes.keys()]
    print(name_nodes)

    dico_states_de_base = extract_states_de_base(xml_root, nodes)
    print(dico_states_de_base)
    # add the base nodes with beautify names in box shape with color
    if river != "True":
        text_initial = [f"{name_nodes[i]} : {nodes[name_nodes[i]][dico_states_de_base['initial'][i]]}" for i in
                        range(len(name_nodes))]
        text_initial = ", ".join(map(str, text_initial))
        text_final = [f"{name_nodes[i]} : {nodes[name_nodes[i]][dico_states_de_base['final'][i]]}" for i in
                      range(len(name_nodes))]
        text_final = ", ".join(map(str, text_final))

    else:
        text_initial = ""
        text_final = ""
        for i in range(len(name_nodes)):
            keys = name_nodes[i]
            value_node_i = nodes[keys][dico_states_de_base['initial'][i]]
            value_node_f = nodes[keys][dico_states_de_base['final'][i]]

            if value_node_i > 1:
                text_initial += f"{value_node_i} {keys}, "
            elif value_node_i == 1:
                text_initial += f"{keys}, "
            if value_node_f > 1:
                text_final += f"{value_node_f} {keys}, "
            elif value_node_f == 1:
                text_final += f"{keys}, "
            else:
                text_final += f"{keys}, "
        text_initial = text_initial[:-2]
        text_final = text_final[:-2]

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
                    if value_node_i > 1:
                        initial_values_g += f"{value_node_i} {keys}, "
                    elif value_node_i == 1:
                        initial_values_g += f"{keys}, "
                    else:
                        initial_values_d += f"{keys}, "
                initial_values_g = initial_values_g[:-2]
                initial_values_d = initial_values_d[:-2]
                initial_values_str = f"{initial_values_g} | {initial_values_d}"

            print(final_values)
            print(final_values == dico_states_de_base["final"])

            if final_values == dico_states_de_base["final"]:
                final_values_str = "final"

            else:
                final_values_g = ""
                final_values_d = ""
                for i in range(len(nodes)):
                    keys = name_nodes[i]
                    value_node_f = final_values[i]
                    if value_node_f > 1:
                        final_values_g += f"{value_node_f} {keys}, "
                    elif value_node_f == 1:
                        final_values_g += f"{keys}, "
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

    #     get the name of the graph
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

    print(f"nodes {nodes}\n")
    print(f"edges {edges}\n")

    initial_edges = {}
    final_edges = {}
    edges_name = []

    for node in edges:
        node_type = node.split(" ")[0]
        node_data = node.split("label=")[1].split("\"")[1]
        node_part = node_data.split(", ")
        node_name = []
        node_value = []
        for part in node_part:
            node_name.append(part.split(" : ")[0])
            node_value.append(part.split(" : ")[1])
        edges_name = node_name
        if node_type == "initial":
            for i in range(len(node_name)):
                initial_edges[f"i{node_name[i]}"] = node_value[i]
        else:
            for i in range(len(node_name)):
                final_edges[f"f{node_name[i]}"] = node_value[i]

    print(f"initial_edges {initial_edges}\n")
    print(f"final_edges {final_edges}\n")
    print(f"edges_name {edges_name}\n")


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
