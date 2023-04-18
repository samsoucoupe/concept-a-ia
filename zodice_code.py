# usr/bin/env python3
import sys
import xml.etree.ElementTree as ET
from graphviz import Digraph, Source


def dot_to_xml(dot_filename, xml_filename):
    dot_graph = Source.from_file(dot_filename)
    graph = ET.Element('graph')

    for edge in dot_graph.edges:
        xml_edge = ET.SubElement(graph, 'edge')
        xml_edge.set('from', edge[0])
        xml_edge.set('to', edge[1])

    tree = ET.ElementTree(graph)
    tree.write(xml_filename, encoding='utf-8', xml_declaration=True)


def xml_to_dot(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    dot = "digraph {\n"

    # create nodes
    for var in root.findall("./variables/var[@type='int extensional']"):
        dot += f"  {var.get('id')} [label=\"{var.text}\"];\n"

    # create edges
    transitions = root.find("./values/valmatrix[@id='transitions']")
    for i, row in enumerate(transitions.findall("./data")):
        for j, value in enumerate(row.text.split()):
            if value == "1":
                print(root[1].text)
                from_var = root.find(f"./variables/vararray[@id='state']/var[{i+1}]")
                to_var = root.find(f"./variables/vararray[@id='state']/var[{j+1}]")
                dot += f"  {from_var} -> {to_var};\n"

    dot += "}"

    with open(output_file, "w") as f:
        f.write(dot)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python3 converter.py [dot_to_xml | xml_to_dot] input_filename output_filename")
        sys.exit(1)

    operation, input_filename, output_filename = sys.argv[1:]

    if operation == 'dot_to_xml':
        dot_to_xml(input_filename, output_filename)
    elif operation == 'xml_to_dot':
        xml_to_dot(input_filename, output_filename)
    else:
        print("Invalid operation. Use 'dot_to_xml' or 'xml_to_dot'.")
        sys.exit(1)