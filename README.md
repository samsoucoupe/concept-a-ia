# Readme du Projet "Concept_IA_Ben_dhiab_Roblin"

Ce Readme fournit des informations sur le projet "Concept_IA_Ben_dhiab_Roblin" et explique comment le configurer et l'exécuter correctement.

## I. Introduction

Ce projet a pour objectif d'appliquer les concepts de base de l'Intelligence Artificielle en utilisant un script Python. Les principales tâches du projet comprenaient :

1. Compléter des fichiers .XML pour deux problèmes : "Loup Chèvre Salade Bateau" et "Sceaux à combiner à la manière de Die Hard".
2. Établir un lien entre la table de transition et le graphe des transitions, permettant de convertir un fichier .XML en .DOT et vice versa.
3. Associer chaque solution trouvée par le solveur à l'affichage en .DOT.
4. Imaginer une interface conviviale pour utiliser l'ensemble du projet.

## II. Déroulement

Le déroulement du projet s'est effectué en plusieurs étapes :

1. Complétion des fichiers .XML : Nous avons établi des règles logiques pour obtenir les résultats souhaités de manière optimisée dans des fichiers .XML utilisables ultérieurement.
2. Transition XML vers DOT : Nous avons travaillé sur la conversion des fichiers .XML en .DOT, permettant ainsi de générer des images PNG claires représentant nos problèmes. Nous avons également travaillé simultanément sur la conversion XML vers DOT et sur la présentation des résultats en PNG.
3. Transition DOT vers XML : Une fois le travail réalisé dans un sens, nous avons développé la conversion inverse, c'est-à-dire du format DOT vers XML.
4. Phase d'optimisation : Cette phase a été la plus longue et la plus complexe du projet. Notre objectif principal était d'obtenir un script propre, produisant des résultats précis et prenant en compte un maximum de paramètres. Nous avons amélioré l'interface en affichant le nom des variables avec une barre en mode River, afin de rendre le script convivial pour l'utilisateur. Cependant, cela a entraîné quelques problèmes lors de la conversion de DOT à XML, car l'accès direct aux valeurs de chaque variable à chaque étape n'était plus possible. Nous avons donc dû définir des règles spécifiques pour la phase initiale et finale de la conversion. Pour optimiser davantage l'interface, nous avons également ajouté des questions permettant à l'utilisateur de définir précisément ses besoins tout en restant dans un environnement contrôlé. Dans un souci d'efficacité, nous avons décidé dès le début du projet de générer des tables automatiquement à l'aide d'un générateur de table. Cela nous a évité un travail fastidieux et répétitif. Les fichiers XML générés ont ensuite été adaptés en fonction des questions posées, permettant de choisir les paramètres pour chaque problème sélectionné.

## III. Configuration et Exécution

Avant de lancer le projet, veuillez suivre les étapes suivantes :

1. Dézippez le répertoire contenant le projet.
2. Accédez au répertoire décompressé à l'aide de la commande 
```
cd .\Concept_IA_Ben_dhiab_Roblin\`.
```
3. Installez les dépendances requises en exécutant la commande 
```
pip install -r .\requirements.txt`.
```

Pour lancer le projet, utilisez la commande suivante :

```
python3 main.py
```

Pour lancer le convertisseur, utilisez la commande suivante :

```
python3 converter.py -r <river> -type <type [xtd, dtx]> -i <input file> -o <output file>
```

**Note :** Remplacez les placeholders `<river>`, `<type [xtd, dtx]>`, `<input file>` et `<output file>` par les valeurs appropriées.

Ceci conclut le Readme du projet "Concept_IA_Ben_dhiab_Roblin". Assurez-vous de suivre les instructions fournies pour configurer et exécuter le projet correctement.
