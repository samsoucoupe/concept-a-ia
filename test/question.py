import json

separateur = "----------------------------"
actions = {"vider":0,"remplir":0,"transferer":0}

type_de_probleme=input("type de probleme: [sceau, river] ") #Choisi le type de problème
while type_de_probleme!="sceau" and type_de_probleme!="river": #Force à choisir que l'un des deux
    type_de_probleme=input("type de probleme: [sceau, river] ")

boat=input("Bateau peut moove solo ? (oui ou non)")#si si il y a un bateau ou non
while boat!="oui" and boat!="non": #Force à choisir que l'un des deux
    boat=input("Bateau peut moove solo ? (oui ou non) ")

boat=boat=="oui" #Transforme en booléen
boat=str(boat) #Transforme en str

boat_size=1


print(separateur)




if type_de_probleme=="sceau":
    nb_element=input("Nombre de sceau: ") #3 S5 S8 S12
    while not nb_element.isdigit(): #Force à rentrer un int
        nb_element=input("Nombre de sceau: ")
else:
    nb_element=input("Nombre d'element distinct: ")  #3 Loup Chèvre Salade
    while not nb_element.isdigit(): #Force à rentrer un int
        nb_element=input("Nombre d'element distinct: ")

nb_element=int(nb_element) #Transformation en int
liste_element= {"element":{},"info_problem":{"type":type_de_probleme,"actions_possible":actions,"position_initial":[],"position_final":[],"boat_only":boat,"boat_size":boat_size,"regle_obligatoire":None}} #Création du dictionnaire
print(separateur)


# liste_element["element"]={0: {'name': 'Loup', 'quantite': '0,1', 'incompatible': [], 'poids': 1.0}, 1: {'name': 'Chevre', 'quantite': '0,1', 'incompatible': [], 'poids': 1.0}, 2: {'name': 'Salade', 'quantite': '0,1', 'incompatible': [], 'poids': 1.0}}
nb_version=1
for i in range(nb_element):
    if type_de_probleme=="sceau":
        print(f"Sceau {i+1} - ")
        taille_sceau=input("Quantité max du sceau: ") #Taille de chaque sceau
        while not taille_sceau.isdigit(): #Force à rentrer un int
            taille_sceau=input("Quantité max du sceau: ")
        name= f"S{taille_sceau}" #Nom de chaque sceau (ex : S5)
        liste_name_use=[]
        for elt in liste_element["element"]:
            liste_name_use.append(liste_element["element"][elt]["name"])
        while name in liste_name_use:
            name= f"S{taille_sceau} ({nb_version})"
            nb_version+=1
        min_value=0 #Valeur min de chaque sceau
        max_value=taille_sceau #Valeur max de chaque sceau
        quantite=str(min_value)+","+str(max_value) #Format min max pour les rules
        liste_element["element"][i]={"name":name,"quantite":quantite,"incompatible":""}

    elif type_de_probleme=="river":
        print(f"Element {i+1}")
        name = input("nom : ") #Nom de chaque élément

        liste_name_use=[]
        for elt in liste_element["element"]:
            liste_name_use.append(liste_element["element"][elt]["name"])
        while name in liste_name_use:
            name= f"{name} ({nb_version})"
            nb_version+=1

        valeur_min = input("valeur min : ")
        while not valeur_min.isdigit() :
            valeur_min = input("valeur min : ")
        valeur_max = input("valeur max : ")
        while not valeur_max.isdigit() :
            valeur_max = input("valeur max : ")
        nb_max = input(f"combien de {name} peuvent être sur le bateau ? : ")
        while not nb_max.isdigit() :
            nb_max = input(f"combien de {name} peuvent être sur le bateau ? : ")
        nb_max=int(nb_max)
        poids= int(liste_element["info_problem"]["boat_size"])/nb_max
        quantite=str(valeur_min)+","+str(valeur_max) #Format min max pour les rules
        liste_element["element"][i]={"name":name,"quantite":quantite,"incompatible":"","poids":poids}

print(liste_element)

if type_de_probleme=="river": # Questions spécifiques au problème River
    print(separateur)

    if nb_element>1:

        for i in range(nb_element):
            liste_autres=[]
            liste_element["element"][i]["incompatible"] = []
            for j in range(nb_element):

                if i!=j :
                    if i>j and i in liste_element["element"][j]["incompatible"]:
                        liste_element["element"][i]["incompatible"].append(j)
                    else:
                        liste_autres.append(f"{j+1}-{liste_element['element'][j]['name']}")

            print(f"Element {i + 1} - {liste_element['element'][i]['name']} est incompatible avec :", end="")
            if liste_element["element"][i]["incompatible"]!=[]:
                liste_imcompatible=[liste_element["element"][x]["name"] for x in liste_element["element"][i]["incompatible"]]
                txt_incompatible=", ".join(liste_imcompatible)
                print(f" {txt_incompatible}")
            else:
                print(f" rien")

            if len(liste_autres)==1:
                personne=liste_autres[0].split("-")
                question=input(f"Est-ce que {personne[1]} est incompatible avec {liste_element['element'][i]['name']} ? (oui 1 / non 0) : ")
                if question=="1" or question=="oui" or question=="o":
                    incompatible=personne[0]
                else:
                    incompatible=""
            else:
                print(f"\nil peut aussi y avoir {', '.join(liste_autres)}")
                incompatible=input("incompatible : ")



            if " " in incompatible:
                liste_incompatible=incompatible.split(" ")
                for elt in liste_incompatible:
                    liste_element["element"][i]["incompatible"].append(int(elt)-1)
            elif incompatible=="":
                pass
            else:
                liste_element["element"][i]["incompatible"].append(int(incompatible)-1)



if type_de_probleme =="sceau" : #Questions spécifiques au problème Sceau
    print(separateur)

    vider = input("Peut-on vider les sceaux ? (oui 1 / non 0) : ")
    while vider!="1" and vider!="0" and vider!= "oui" and vider!="non":
        vider = input("Peut-on vider les sceaux ? (oui 1 / non 0) : ")
    if vider == "oui":
        actions["vider"] = 1
    elif vider == "non":
        actions["vider"] = 0
    else:
        actions["vider"] = int(vider)

    remplir = input("Peut-on remplir les sceaux ? (oui 1 / non 0) : ")
    while remplir!="1" and remplir!="0" and remplir!= "oui" and remplir!="non":
        remplir = input("Peut-on remplir les sceaux ? (oui 1 / non 0) : ")
    if remplir == "oui":
        actions["remplir"] = 1
    elif remplir == "non":
        actions["remplir"] = 0
    else:
        actions["remplir"] = int(remplir)

    transferer = input("Peut-on transferer les sceaux ? (oui 1 / non 0) : ")
    while transferer!="1" and transferer!="0" and transferer!= "oui" and transferer!="non":
        transferer = input("Peut-on transferer les sceaux ? (oui 1 / non 0) : ")
    if transferer == "oui":
        actions["transferer"] = 1
    elif transferer == "non":
        actions["transferer"] = 0
    else:
        actions["transferer"] = int(transferer)

    liste_element["info_problem"]["actions_possible"]=actions

# parti pour state initial et final
print(separateur)
print("Etat initial :")
initial = []
final = []

if type_de_probleme=="river":

    for i in range(nb_element):
        print(f"Combien y a-t-il de {liste_element['element'][i]['name']} a gauche ?")
        quantite = input("Quantité : ")
        while not quantite.isdigit() :
            quantite = input("Quantité : ")
        initial.append(int(quantite))
    liste_element["info_problem"]["position_initial"]=initial+[1]
    print("Etat final :")
    for i in range(nb_element):
        print(f"Combien y a-t-il de {liste_element['element'][i]['name']} a gauche ?")
        quantite = input("Quantité : ")
        while not quantite.isdigit() :
            quantite = input("Quantité : ")
        final.append(int(quantite))
        position_boat=input("Le bateau est-il à gauche ? (oui 1 / non 0) : ")
        while position_boat!="1" and position_boat!="0" and position_boat!= "oui" and position_boat!="non":
            position_boat = input("Le bateau est-il à gauche ? (oui 1 / non 0) : ")
        if position_boat=="1" or position_boat=="oui" or position_boat=="o":
            final.append(1)
        else:
            final.append(0)
    liste_element["info_problem"]["position_final"]=final

elif type_de_probleme=="sceau":
    for i in range(nb_element):
        print(f"Combien y a-t-il dans {liste_element['element'][i]['name']} ?")
        quantite = input("Quantité : ")
        while not quantite.isdigit() :
            quantite = input("Quantité : ")
        initial.append(int(quantite))
    liste_element["info_problem"]["position_initial"]=initial
    print("Etat final :")
    for i in range(nb_element):
        print(f"Combien y a-t-il dans {liste_element['element'][i]['name']} ?")
        quantite = input("Quantité : ")
        while not quantite.isdigit() :
            quantite = input("Quantité : ")
        final.append(int(quantite))
    liste_element["info_problem"]["position_final"]=final


print(liste_element)
nom_fichier=input("Nom du fichier : ")
# Ecriture du fichier json
with open(f"{nom_fichier}.json", "w") as f:
    json.dump(liste_element, f, indent=4)
