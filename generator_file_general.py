import sys
import xml.etree.ElementTree as ET
def main(name):
        lien_xml=f"{name}.xml"
        lien_data=f"{name}_data.txt"


        # Créer la racine du document XML
        root = ET.Element("instance", format="Talos")

        # Ajouter les valeurs du document
        values = ET.SubElement(root, "values")

        valmatrix = ET.SubElement(values, "valmatrix", id="transitions")


        # recupere data de lien_data
        with open(lien_data,'r') as d:
            data = [x for x in d.readlines()[0].split(",")]
        print(data)
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

        tree.write(lien_xml, encoding="utf-8", xml_declaration=True)
        print("Done")

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
    if len(sys.argv) <2 :
        print("Usage: python3 -name name")
        sys.exit(1)

    name=None

    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "-name":
            name = sys.argv[i+1]
            main(name=name)
        else:
            print("Invalid argument. Use -name.")
            sys.exit(1)




