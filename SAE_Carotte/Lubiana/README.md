### Bien le bonjour ! ###

Ce README a pour objectif de vous donner un aperçu complet de ce que permet de faire nos logiciels dans le cadre du projet de la Carotte Electronique !

IMPORTANT = Pour utiliser les programmes, il faut activer l'environnement de développement avec la commande :

"source ./Lubiana/bin/activate"

Rentrons dans le vif du sujet ! Nommons déjà les logiciels présents dans notre dossier. 

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
