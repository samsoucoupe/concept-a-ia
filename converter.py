import sys
import xml.etree.ElementTree as ET
from graphviz import Digraph,Source


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
    nodes= xml_root.find('variables').findall('var[@type="int extensional"]')
    for node in nodes:
        dico_data[node.attrib['id']]=list_of_nodes[nodes.index(node)]
    return dico_data


def xml_to_dot(xml_filename, dot_filename,river):
    tree = ET.parse(xml_filename)
    xml_root = tree.getroot()

    valmatrix_data = extract_data_from_xml(xml_root)
    name=dot_filename.strip(".dot")
    dot_graph = Digraph(name)
    nodes = extract_nodes_from_xml(xml_root)
    print(nodes)
    print("nodes ^")


    name_nodes= [keys for keys in nodes.keys()]
    print(name_nodes)

    print(valmatrix_data)
    print()


    for transition in valmatrix_data:
        initial_values = transition[:len(nodes)]
        final_values = transition[len(nodes):]
        if river=="True":
            # prendre la valeurs et si elle est differentes de 1 on affiche le nombre + l'id du noeud sinon on affiche l'id du noeud

            initial_values_g = []
            initial_values_d = []
            final_values_g = []
            final_values_d = []
            print(initial_values)
            for i in range(len(nodes)):
                keys = name_nodes[i]
                value_node_g=initial_values[i]
                value_node_d=abs(nodes[keys][-1]-value_node_g)
                print(f"value node g {value_node_g}")
                print(f"value node d {value_node_d}")

                if value_node_g > 1:
                    initial_values_g.append(f"{value_node_g} {keys}")
                elif value_node_g == 1:
                    initial_values_g.append(keys)


                if value_node_d > 1:
                    initial_values_d.append(f"{value_node_d} {keys}")
                elif value_node_d == 1:
                    initial_values_d.append(keys)

                value_node_g=final_values[i]
                value_node_d=abs(nodes[keys][-1]-value_node_g)
                print(f"value node g {value_node_g}")
                print(f"value node d {value_node_d}")

                if value_node_g > 1:
                    final_values_g.append(f"{value_node_g} {keys}")
                elif value_node_g == 1:
                    final_values_g.append(keys)

                if value_node_d > 1:
                    final_values_d.append(f"{value_node_d} {keys}")
                elif value_node_d == 1:
                    final_values_d.append(keys)

            initial_values_g_str = ", ".join(map(str, initial_values_g))
            initial_values_d_str = ", ".join(map(str, initial_values_d))
            initial_values_str = f"{ initial_values_g_str} | { initial_values_d_str }"

            final_values_g_str = ", ".join(map(str, final_values_g))
            final_values_d_str = ", ".join(map(str, final_values_d))
            final_values_str = f"{ final_values_g_str} | { final_values_d_str }"



            dot_graph.edge(initial_values_str, final_values_str)

        else:
            initial_values_str = ", ".join(map(str, initial_values))
            final_values_str = ", ".join(map(str, final_values))
            dot_graph.edge(initial_values_str, final_values_str)


    with open(dot_filename, "w") as f:
        f.write(dot_graph.source)


def dot_to_xml(input_filename, output_filename):
    pass


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
            river = sys.argv[i+1]
        elif sys.argv[i] == "-type":
            operation = sys.argv[i+1]
        elif sys.argv[i] == "-input":
            input_filename = sys.argv[i+1]
        elif sys.argv[i] == "-output":
            output_filename = sys.argv[i+1]
        else:
            print("Invalid argument. Use -r, -type, -input, -output.")
            sys.exit(1)


    if operation == "xtd":
        print("Converting XML to DOT...")
        print(f"Input file: {input_filename}")
        print(f"Output file: {output_filename}")
        print(f"River: {river}")

        xml_to_dot(xml_filename=input_filename, dot_filename=output_filename,river=river)
    elif operation == "dtx":
        dot_to_xml(input_filename, output_filename)
    else:
        print("Invalid operation. Use 'xtd' or 'dtx'.")
        sys.exit(1)
