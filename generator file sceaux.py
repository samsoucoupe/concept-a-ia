import xml.etree.ElementTree as ET

# Créer la racine du document XML
root = ET.Element("instance", format="Talos")

# Ajouter les valeurs du document
values = ET.SubElement(root, "values")

valmatrix = ET.SubElement(values, "valmatrix", id="transitions")

data=[
"0 0 5 0",
"0 0 0 3",
"0 3 5 3",
"0 3 0 0",
"0 3 3 0",
"3 0 0 0",
"3 0 5 0",
"3 0 0 3",
"3 0 3 3",
"3 3 0 3",
"3 3 5 3",
"3 3 3 0",
"3 3 5 1",
"5 1 0 1",
"5 1 3 3",
"5 1 5 0",
"5 1 5 3",
"5 3 0 3",
"5 3 5 0",
"5 0 0 0",
"5 0 2 3",
"5 0 5 3",
"2 3 0 3",
"2 3 5 3",
"2 3 2 0",
"2 3 5 0",
"2 0 0 0",
"2 0 5 0",
"2 0 0 2",
"2 0 2 3",
"0 2 5 2",
"0 2 0 0",
"0 2 0 3",
"0 2 2 0",
"5 2 0 2",
"5 2 4 3",
"5 2 5 0",
"5 2 5 3",
"4 3 0 3",
"4 3 5 3",
"4 3 4 0",
"4 3 5 2",
"4 0 0 0",
"4 0 5 0",
"4 0 1 3",
"4 0 4 3",
"1 3 0 3",
"1 3 5 3",
"1 3 1 0",
"1 3 4 0",
"1 0 0 0",
"1 0 5 0",
"1 0 0 1",
"1 0 1 3",
"0 1 5 1",
"0 1 0 0",
"0 1 0 3",
"0 1 1 0"
]

for row in data:
    ET.SubElement(valmatrix, "data").text = row

# Ajouter les variables du document
variables = ET.SubElement(root, "variables")

var = ET.SubElement(variables, "var", id="iS5")
var.text = "0"
var = ET.SubElement(variables, "var", id="iS3")
var.text = "0"
var = ET.SubElement(variables, "var", id="fS5")
var.text = "4"
var = ET.SubElement(variables, "var", id="fS3")
var.text = "0"

var = ET.SubElement(variables, "var", id="S5", type="int extensional")
var.text = "0 1 2 3 4 5"
var = ET.SubElement(variables, "var", id="S3", type="int extensional")
var.text = "0 1 2 3"

# Ajouter les variables du document
variables = ET.SubElement(root, "variables")

vararray = ET.SubElement(variables, "vararray", id="state")
vararray.text = "S5 S3"

vararray = ET.SubElement(variables, "vararray", id="initial")
vararray.text = "iS5 iS3"

vararray = ET.SubElement(variables, "vararray", id="final")
vararray.text = "fS5 fS3"
# Générer le fichier XML
tree = ET.ElementTree(root)
lien = "sceau.xml"
tree.write(lien, encoding="utf-8", xml_declaration=True)
print("Done")

# ajouter standalone="no" dans la ligne xml_declaration=True pour générer un fichier valide
lignes = []
with open(lien, "r") as file:
    data = file.read()
    lignes = data.split("\n")

with open(lien, "w") as file:
    for ligne in lignes:
        if ligne.startswith("<?xml"):
            ligne = ligne.replace("?>", " standalone=\"no\"?>")
            file.write(ligne + "\n")
        else:
            file.write(ligne + "\n")
