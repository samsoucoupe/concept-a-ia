import sys
import xml.etree.ElementTree as ET
from graphviz import Digraph


def extract_data_from_xml(xml_root):
    valmatrix_data = [
        list(map(int, data.text.split()))
        for data in xml_root.find("values").find("valmatrix").findall("data")
    ]

    return valmatrix_data


def xml_to_dot(xml_filename, dot_filename):
    tree = ET.parse(xml_filename)
    xml_root = tree.getroot()

    valmatrix_data = extract_data_from_xml(xml_root)

    dot_graph = Digraph()
    nodes = xml_root.find('variables').findall('var[@type="int extensional"]')
    # for node in nodes:
    #     dot_graph.node(node.get('id'), shape='box')

    print(valmatrix_data)
    print()
    for elt in nodes:
        print(elt.attrib['id'])
    print()

    for transition in valmatrix_data:
        # for j in range(len(nodes)):
        #     print(f"{nodes[j].attrib['id']} intial value = {transition[j]} and final value = {transition[len(nodes)+j]}")
        #     if transition[j] != transition[len(nodes)+j]:
        #         lab= f"{transition[j]} -> {transition[len(nodes)+j]}"
        #         dot_graph.edge(nodes[j].attrib['id'], nodes[j].attrib['id'], label=lab)
        initial_values = transition[:len(nodes)]
        final_values = transition[len(nodes):]

        initial_values_g = [nodes[i].attrib['id'] for i in range(len(nodes)) if initial_values[i] == 1]
        initial_values_d= [nodes[i].attrib['id'] for i in range(len(nodes)) if initial_values[i] == 0]
        initial_values_g_str = ", ".join(map(str, initial_values_g))
        initial_values_d_str = ", ".join(map(str, initial_values_d))
        intial_values_str = f"{ initial_values_g_str}  | { initial_values_d_str }"

        final_values_g = [nodes[i].attrib['id'] for i in range(len(nodes)) if final_values[i] == 1]
        final_values_d= [nodes[i].attrib['id'] for i in range(len(nodes)) if final_values[i] == 0]
        final_values_g_str = ", ".join(map(str, final_values_g))
        final_values_d_str = ", ".join(map(str, final_values_d))
        final_values_str = f"{ final_values_g_str}  | { final_values_d_str }"

        dot_graph.edge(intial_values_str, final_values_str)



    with open(dot_filename, "w") as f:
        f.write(dot_graph.source)





if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 converter.py input_filename output_filename")
        sys.exit(1)

    input_filename, output_filename = sys.argv[1:]
    xml_to_dot(input_filename, output_filename)
