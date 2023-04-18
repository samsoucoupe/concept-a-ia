import xml.etree.ElementTree as ET
import lxml.etree as TS

# Créer la racine du document XML
root = ET.Element("instance", format="Talos")

# Ajouter les valeurs du document
values = ET.SubElement(root, "values")

valmatrix = ET.SubElement(values, "valmatrix", id="transitions")
data = [
    "1 1 1 1 1 0 1 0",
    "0 1 0 1 0 0 0 0",
    "1 0 1 0 1 0 1 1",
    "1 1 0 1 0 1 0 0",
    "1 1 0 1 1 0 0 0",
    "0 1 1 1 0 0 1 0",
    "0 1 1 1 0 1 0 0",
    "1 0 1 1 0 0 1 0",
    "1 0 1 1 1 0 0 0",
    "1 0 1 1 1 0 1 0",
    "0 1 0 1 0 1 0 0",
    "1 0 1 0 1 1 1 1",
    "0 1 0 0 0 1 0 1",
    "0 1 0 0 0 1 1 1",
    "0 1 0 0 1 1 0 1",
    "1 0 0 0 1 1 0 1",
    "1 0 0 0 1 0 1 1",
    "0 0 1 0 0 1 1 1",
    "0 0 1 0 1 0 1 1",
    "0 0 0 0 0 0 0 0"
]
for row in data:
    ET.SubElement(valmatrix, "data").text = row

# Ajouter les variables du document
variables = ET.SubElement(root, "variables")

var = ET.SubElement(variables, "var", id="iL")
var.text = "1"
var = ET.SubElement(variables, "var", id="iC")
var.text = "1"
var = ET.SubElement(variables, "var", id="iS")
var.text = "1"
var = ET.SubElement(variables, "var", id="iB")
var.text = "1"
var = ET.SubElement(variables, "var", id="fL")
var.text = "0"
var = ET.SubElement(variables, "var", id="fC")
var.text = "0"
var = ET.SubElement(variables, "var", id="fS")
var.text = "0"
var = ET.SubElement(variables, "var", id="fB")
var.text = "0"


var = ET.SubElement(variables, "var", id="L",type="int extensional")
var.text = "0 1"
var = ET.SubElement(variables, "var", id="C",type="int extensional")
var.text = "0 1"
var = ET.SubElement(variables, "var", id="S",type="int extensional")
var.text = "0 1"
var = ET.SubElement(variables, "var", id="B",type="int extensional")
var.text = "0 1"

# Ajouter les variables du document
variables = ET.SubElement(root, "variables")

vararray = ET.SubElement(variables, "vararray", id="state")
vararray.text = "L C S B"

vararray = ET.SubElement(variables, "vararray", id="initial")
vararray.text = "iL iC iS iB"

vararray = ET.SubElement(variables, "vararray", id="final")
vararray.text = "fL fC fS fB"
# Générer le fichier XML
tree = ET.ElementTree(root)
lien = "IA.xml"
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

