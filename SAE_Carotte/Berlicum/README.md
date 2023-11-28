### Bien le bonjour ! ###

Ce README a pour objectif de vous donner un aperçu complet de ce que permet de faire nos logiciels dans le cadre du projet de la Carotte Electronique !

IMPORTANT = Pour utiliser les programmes, il faut activer l'environnement de développement avec la commande :

"source ./Lubiana/bin/activate"

Rentrons dans le vif du sujet ! Nommons déjà les logiciels présents dans notre dossier. 

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
