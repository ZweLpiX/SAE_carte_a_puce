### Bien le bonjour ! ###

Ce README a pour objectif de vous donner un aperçu complet de ce que permet de faire nos logiciels dans le cadre du projet de la Carotte Electronique !

IMPORTANT = Pour utiliser les programmes, il faut activer l'environnement de développement avec la commande :

"source ./Lubiana/bin/activate"

Pour une utilisation plus intuitive, le dossier GRAPHIQUE contient tout ! 
Les étapes : 
- "source répertoire de SAE_Carotte/bin/activate"
- "python3 launcher.py"
- Lancez Rubrovitamin et faites un make clean, make et make progcarte. Assurez-vous que le programmateur est reconnu sur VirtualBox.
- Lancez Lubiana et vous pouvez afficher la version, commencez par renseigner les informations de la carte puis vous pouvez les visualiser, rechargez aussi la carte de 1 Euro. 
- Lancez Rodelika / Rodelika_WEB, vous pourrez renseigner l'étudiant dans la BDD et lui accorder un bonus. Vous pouvez ensuite voir le solde actuel tel qu'il est renseigné dans la BDD. 
- Lancez Berlicum et vous pourrez transférer le solde bonus sur la carte. Il est aussi possible de charger la carte avec sa CB.
- Lancez Distributeur pour les boissons à 20 cts.

Rentrons dans le vif du sujet ! Nommons déjà les logiciels présents dans notre dossier. 

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Rubrovitamin : 
- Contient rubrovitamin.c : ce code permet de mettre en place le contexte de ce qu'on va programmer sur la carte. On y retrouve l'initialisation de données pour l'EEPROM, des variables globales et des fonctions. Dans les grandes lignes, cela inclut la procédure pour mettre en place l'ATR, l'enregistrement de la version d'application, l'écriture et la visualisation des données de l'étudiant.

Fonctionnalités : "make", "make progcarte", "make clean". 
Dans le répertoire Rubrovitamin : la commande "make" permet de générer les fichiers nécessaires pour programmer la carte. "make progcarte" permet de programmer la carte. "make clean" permet de nettoyer les fichiers générés avec la commande make.

HOWTOUSE : On peut lancer l'interface graphique avec la commande : python3 Rubro_GUI.py qui permet de mieux visualiser toutes ces options. 

ATTENTION ! Pour utiliser Rubrovitamin, il faut que la carte soit dans le programmateur et reconnue par VirtualBox. Pensez à activer le périphérique dans les paramètres USB 3.0 de VirtualBox.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Lubiana : 
- Contient lubiana.py : ce code permet visualiser la version de l'application, pour le moment fixée à 1.0. On peut également observer les informations personnelles de l'étudiant (seconde fonctionnalité). La troisième option permet justement de renseigner ces informations (nom, prénom et date de naissance). On peut ensuite recharger 1 euro sur la carte, ce qui correspond au solde initial. Pour conclure, on peut consulter le solde de la carte. Il est constamment à jour par rapport aux autres logiciels. Ce qu'il faut comprendre par là c'est qu'il permettra de vérifier que le solde initial a bien été versé, qu'il ne l'a été qu'une fois, et également qu'entre temps si on a utilisé la carte, le solde sera à jour. 

HOWTOUSE : On peut lancer l'interface graphique avec la commande : "python3 LubianaGUI.py", l'interface par ligne de commande fonctionne avec "python3 lubiana.py".

Options : 
- 1 : Afficher la version = 1.0
- 2 : Afficher les données = Nom, prénom et date de naissance
- 3 : Attribuer la carte = les informations de l'étudiant, ce qu'on visualise avec l'option précédente. 
- 4 : Recharger 1E sur la carte = rentrer le solde initial de l'étudiant
- 5 : Consulter le solde = information à jour, valeur à 1E au moment de l'attribution de la carte une fois qu'on a versé le solde initial.

ATTENTION ! Pour utiliser Lubiana, il faut que la carte soit dans le lecteur et reconnue par VirtualBox. Pensez à activer le périphérique dans les paramètres USB 3.0 de VirtualBox.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Rodelika : 
- Contient Rodelika.py : ce code fait un lien direct avec la BDD purpledragon, il propose plusieurs fonctionnalités mais n'interragit pas directement avec la carte. L'idée c'est de lire les données de la BDD et d'écrire dedans. 

HOWTOUSE : On peut lancer l'interface graphique avec la commande : "python3 Rodelika_GUI.py", l'interface par ligne de commande fonctionne avec "python3 Rodelika.py".

Options : 
1 - Liste des étudiants : affiche tous les étudiants enregistrés dans la BDD ainsi que les infos associées.
2 - Solde des étudiants : permet de visualiser les soldes bonus des étudiants
3 - Saisir un nouvel étudiant : sert à rentrer les informations d'un étudiant dans la BDD
4 - Attribuer un bonus : génère un bonus avec un commentaire pour un étudiant en fonction de son ID
5 - Crédits : voir les infos du README sur cette partie logicielle

ATTENTION ! Pour utiliser Rodelika, il faut que la carte soit dans le lecteur et reconnue par VirtualBox. Pensez à activer le périphérique dans les paramètres USB 3.0 de VirtualBox.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Rodelika_WEB : 


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Berlicum : 
- Contient Berlicum.py : ce code permet de faire le pont entre la BDD et les données de la carte. 

HOWTOUSE : On peut lancer l'interface graphique avec la commande : "python3 GUI_Berlicum.py", l'interface par ligne de commande fonctionne avec "python3 Berlicum.py".

Options : 
1 - Afficher mes bonus : lit les bonus renseignés dans la BDD purpledragon. Cette option vérifie d'abord que l'étudiant qui utilise la carte (donc les données de la carte) correspondent à une entrée dans la BDD pour un étudiant.
2 - Afficher le solde actuel sur la carte : permet de voir le solde déjà transféré et utilisable. 
3 - Convertir les bonus : sert à transférer la somme des bonus sur la carte et efface les entrées des bonus dans la BDD.
4 - Recharger avec ma carte bancaire : échange de messages avec une CB fictive pour transférer des sous sur sa carte.

ATTENTION ! Pour utiliser Berlicum, il faut que la carte soit dans le lecteur et reconnue par VirtualBox. Pensez à activer le périphérique dans les paramètres USB 3.0 de VirtualBox.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Machine à café : 
- Contient café.py : ce code permet soustraire 20 cts à chaque boisson préparée.

HOWTOUSE : On peut lancer l'interface graphique avec la commande : "python3 GUI_café.py", l'interface par ligne de commande fonctionne avec "python3 café.py".

Options : 
PRIX DES BOISSONS: 0.20 € 
1 - Café
2 - Thé
3 - Chocolat Chaud
4 - Quitter

ATTENTION ! Pour utiliser Machine à café, il faut que la carte soit dans le lecteur et reconnue par VirtualBox. Pensez à activer le périphérique dans les paramètres USB 3.0 de VirtualBox.
