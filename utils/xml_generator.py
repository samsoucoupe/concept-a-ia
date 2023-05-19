#  Copyright (c) 2023. Samy Ben Dhiab (Samsoucoupe) All rights reserved.
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
#


import sys
import xml.etree.ElementTree as ET


def generator(name, initial=None, final=None, data=None, node_names=None, possible_value=None, test=False):
    lien_xml = name

    # Créer la racine du document XML
    root = ET.Element("instance", format="Talos")

    # Ajouter les valeurs du document
    values = ET.SubElement(root, "values")

    valmatrix = ET.SubElement(values, "valmatrix", id="transitions")

    for row in data:
        ET.SubElement(valmatrix, "data").text = row

    # Ajouter les variables du document
    variables = ET.SubElement(root, "variables")
    for i in range(len(node_names)):
        var = ET.SubElement(variables, "var", id=f"i{node_names[i]}")
        var.text = str(initial[i])
    for i in range(len(node_names)):
        var = ET.SubElement(variables, "var", id=f"f{node_names[i]}")
        var.text = str(final[i])
    for i in range(len(node_names)):
        var = ET.SubElement(variables, "var", id=f"{node_names[i]}", type="int extensional")
        var.text = str(" ".join(map(str, possible_value[i])))

    # Ajouter les variables du document
    variables = ET.SubElement(root, "variables")

    vararray = ET.SubElement(variables, "vararray", id="state")
    vararray.text = str(" ".join(map(str, node_names)))

    temp_node_name = ["i" + x for x in node_names]
    vararray = ET.SubElement(variables, "vararray", id="initial")
    vararray.text = str(" ".join(map(str, temp_node_name)))

    temp_node_name = ["f" + x for x in node_names]
    vararray = ET.SubElement(variables, "vararray", id="final")
    vararray.text = str(" ".join(map(str, temp_node_name)))
    # Générer le fichier XML
    tree = ET.ElementTree(root)

    tree.write(lien_xml, encoding="utf-8", xml_declaration=True)

    # ajouter standalone="no" dans la ligne xml_declaration=True pour générer un fichier valide
    lignes = []
    with open(lien_xml, "r") as file:
        data = file.read()
        lignes = data.split("\n")

    with open(lien_xml, "w") as file:
        for ligne in lignes:
            if ligne.startswith("<?xml"):
                ligne = ligne.replace("?>", " standalone=\"no\"?>")
                file.write(ligne + "\n")
            else:
                file.write(ligne + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 -name name")
        sys.exit(1)

    name = None
    test = False

    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "-name":
            name = sys.argv[i + 1]
        elif sys.argv[i] == "-t":
            test = True
        else:
            print("Invalid argument. Use -name.")
            sys.exit(1)
        if name is not None:
            generator(name=name, test=test)
