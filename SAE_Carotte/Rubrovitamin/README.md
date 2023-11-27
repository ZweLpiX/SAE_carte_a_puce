### Bien le bonjour ! ###

Ce README a pour objectif de vous donner un aperçu complet de ce que permet de faire nos logiciels dans le cadre du projet de la Carotte Electronique !

IMPORTANT = Pour utiliser les programmes, il faut activer l'environnement de développement avec la commande :

"source chemin jusqu'à Rubrovitamin /Rubrovitamin/bin/activate"

Vous pouvez également vous contentez de lancer le script shell conscaré à Rubrovitamin.

Rentrons dans le vif du sujet ! Nommons déjà les logiciels présents dans notre dossier. 

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Rubrovitamin : 
- Contient rubrovitamin.c : ce code permet de mettre en place le contexte de ce qu'on va programmer sur la carte. On y retrouve l'initialisation de données pour l'EEPROM, des variables globales et des fonctions. Dans les grandes lignes, cela inclut la procédure pour mettre en place l'ATR, l'enregistrement de la version d'application, l'écriture et la visualisation des données de l'étudiant.

Fonctionnalités : "make", "make progcarte", "make clean". 
Dans le répertoire Rubrovitamin : la commande "make" permet de générer les fichiers nécessaires pour programmer la carte. "make progcarte" permet de programmer la carte. "make clean" permet de nettoyer les fichiers générés avec la commande make.

HOWTOUSE : On peut lancer l'interface graphique avec la commande : python3 Rubro_GUI.py qui permet de mieux visualiser toutes ces options. 

ATTENTION ! Pour utiliser Rubrovitamin, il faut que la carte soit dans le programmateur et reconnue par VirtualBox. Pensez à activer le périphérique dans les paramètres USB 3.0 de VirtualBox.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
