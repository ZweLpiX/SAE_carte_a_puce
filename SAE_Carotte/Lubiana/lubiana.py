# Importation des librairies 

import smartcard.System as scardsys
import smartcard.util as scardutil
import smartcard.Exceptions as scardexcp

import re
import time
import tkinter as tk
from tkinter import simpledialog
from smartcard.System import readers
from smartcard.Exceptions import CardConnectionException

#Partie Smart Card

#Modification de la fonction init_smart_card

def init_smart_card():
    try:
        lst_readers = scardsys.readers()
        if not lst_readers:
            print("Pas de lecteur de carte connecté !")
            exit()

        global conn_reader
        conn_reader = lst_readers[0].createConnection()

        try:
            conn_reader.connect()
            # La connexion réussie est établie, mais le message n'est pas imprimé
        except scardexcp.CardConnectionException as e:
            print(f"Erreur lors de la tentative de connexion : {e}")
            print("Tentative de reconnexion après un délai...")
            time.sleep(2)  # Attendre 2 secondes avant de réessayer
            try:
                conn_reader.connect()
                # Reconnexion réussie, mais le message n'est pas imprimé
            except scardexcp.CardConnectionException as e:
                print(f"Échec de la reconnexion : {e}")
                exit()

        global card_atr
        card_atr = conn_reader.getATR()
        # L'ATR de la carte est obtenu, mais le message n'est pas imprimé

    except Exception as e:
        print(f"Erreur lors de l'initialisation de la carte : {e}")
        exit()

    return

global is_card_assigned
is_card_assigned = False
#Créations des fonctions différentes 

#Fonction affichant la version
def print_version():
    apdu = [0x81, 0x00, 0x00, 0x00, 0x04]
    data, sw1, sw2 = conn_reader.transmit(apdu)
    if sw1 == 0x90 and sw2 == 0x00:
        version = ''.join(chr(e) for e in data)
        print("\nVersion de la carte : ", version)
    else:
        print("\nErreur lors de la lecture de la version de la carte.")

#Fonction affichant le nom de l'utilisateur de la carte


def print_nom():
    try:
        apdu = [0x81, 0x02, 0x00, 0x00, 0x00]
        data, sw1, sw2 = conn_reader.transmit(apdu)
        apdu[4] = sw2
        data, sw1, sw2 = conn_reader.transmit(apdu)
        return ''.join(chr(e) for e in data) if data else ''
    except CardConnectionException:
        return "Erreur lors de la transmission avec la carte."

def print_prenom():
    try:
        apdu = [0x81, 0x04, 0x00, 0x00, 0x00]
        data, sw1, sw2 = conn_reader.transmit(apdu)
        apdu[4] = sw2
        data, sw1, sw2 = conn_reader.transmit(apdu)
        return ''.join(chr(e) for e in data) if data else ''
    except CardConnectionException:
        return "Erreur lors de la transmission avec la carte."

def print_birth():
    try:
        apdu = [0x81, 0x06, 0x00, 0x00, 0x00]
        data, sw1, sw2 = conn_reader.transmit(apdu)
        apdu[4] = sw2
        data, sw1, sw2 = conn_reader.transmit(apdu)
        return ''.join(chr(e) for e in data) if data else ''
    except CardConnectionException:
        return "Erreur lors de la transmission avec la carte."


#Fonctions permettant d'attribuer la carte
#Nom 
def intro_nom():
    apdu = [0x81, 0x01, 0x00, 0x00]
    while True:
        nom = input("Saisissez le Nom de l'élève : ")
        if is_valid_name(nom):
            break
        else:
            print("Nom invalide. Veuillez entrer un nom valide.")

    length_nom = len(nom)
    apdu.append(length_nom)
    for e in nom:
        apdu.append(ord(e))

    return send_and_validate(apdu, "Nom de l'élève", nom)

#Prénom 
def intro_prenom():
    apdu = [0x81, 0x03, 0x00, 0x00]
    while True:
        prenom = input("Saisissez le Prénom de l'élève : ")
        if is_valid_name(prenom):
            break
        else:
            print("Prénom invalide. Veuillez entrer un prénom valide.")

    length_prenom = len(prenom)
    apdu.append(length_prenom)
    for e in prenom:
        apdu.append(ord(e))

    return send_and_validate(apdu, "Prénom de l'élève", prenom)

def send_and_validate(apdu, field_name, field_value):
    try:
        data, sw1, sw2 = conn_reader.transmit(apdu)
        if sw1 == 0x90:
            print(f"\n{field_name} enregistré avec succès.")
            return field_value
        else:
            print(f"Erreur lors de l'enregistrement de {field_name} : {sw1}")
            return None  # Retourner None en cas d'échec
    except scardexcp.CardConnectionException as e:
        print(f"Erreur de transmission : {e}")
        return None  # Retourner None en cas d'exception
        
#Date de naissance
def is_valid_date(date):
    """ Vérifie si la date est valide selon le format JJMMAAAA. """
    if re.match(r'\d{2}\d{2}\d{4}', date):
        day, month, year = int(date[:2]), int(date[2:4]), int(date[4:])
        return 1 <= day <= 31 and 1 <= month <= 12 and 1950 <= year <= 2010
    return False

def is_valid_name(name):
    """ Vérifie si le nom est valide selon les critères. """
    return re.match(r'^[A-Z][a-z]{0,9}$', name) is not None

def is_valid_name(prenom):
    """ Vérifie si le nom est valide selon les critères. """
    return re.match(r'^[A-Z][a-z]{0,9}$', prenom) is not None

def intro_birth():
    apdu = [0x81, 0x05, 0x00, 0x00]

    while True:
        birth = input("Saisissez la date de naissance (Format : JJMMAAAA) : ")
        if is_valid_date(birth):
            break
        else:
            print("Merci de mettre une date valide.")

    length_birth = len(birth)
    apdu.append(length_birth)
    for e in birth:
        apdu.append(ord(e))

    return send_and_validate(apdu, "Date de naissance", birth)

def send_and_validate(apdu, field_name, field_value):
    try:
        data, sw1, sw2 = conn_reader.transmit(apdu)
        if sw1 == 0x90:
            print(f"\n{field_name} enregistré avec succès.")
            return field_value  # Retourner la valeur saisie en cas de succès
        else:
            print(f"Erreur lors de l'enregistrement de {field_name} : {sw1}")
            return None
    except scardexcp.CardConnectionException as e:
        print(f"Erreur de transmission : {e}")
        return None
        
        
#Fonction permettant de récuperer le solde de la carte
def get_balance():
    # APDU pour lire le solde de la carte
    apdu = [0x82, 0x01, 0x00, 0x00, 0x02]  # Commande pour la lecture du solde
    data, sw1, sw2 = conn_reader.transmit(apdu)  # Envoi de la commande à la carte
    apdu[4] = sw2 # Met à jour le cinquième octet de l'instruction qui correspond à l'octet SW2
    data, sw1, sw2 = conn_reader.transmit(apdu) # On renvoie la commande et on récupère ses données
    str = ""
    for e in data:
        str += chr(e)
    print ("""
        Solde : %s €""" % (str))    
    return

#Fonction permettant de mettre le solde initial à la carte
def recharge_card():
    solde = '1.00'
    # APDU pour créditer la carte avec un montant spécifié
    apdu = [0x82, 0x02, 0x00, 0x00, 0x05]  # Commande pour créditer la carte
    length_solde = len(solde)
    apdu.append(length_solde)
    for e in solde:
        apdu.append(ord(e))

    try:
        data, sw1, sw2 = conn_reader.transmit(apdu)  # Envoi de la commande à la carte
        if sw1 == 0x90:  # Si la commande s'est exécutée avec succès
            print(f"La carte a été créditée avec succès de {solde}€.")
        else:
            print(f"Erreur lors du rechargement de la carte : SW1=0x{sw1:02X}, SW2=0x{sw2:02X}")
    except scardexcp.CardConnectionException as e:
        print("Erreur : ", e)
    return

#Création du menu


#Modification du message de bienvenue
def print_hello_message():
    print("""

 ____                              _                      _                          
| __ )  ___  _ __ _ __   ___    __| | ___   _ __ ___  ___| |__   __ _ _ __ __ _  ___ 
|  _ \ / _ \| '__| '_ \ / _ \  / _` |/ _ \ | '__/ _ \/ __| '_ \ / _` | '__/ _` |/ _ \ \t
| |_) | (_) | |  | | | |  __/ | (_| |  __/ | | |  __/ (__| | | | (_| | | | (_| |  __/
|____/ \___/|_|  |_| |_|\___|  \__,_|\___| |_|  \___|\___|_| |_|\__,_|_|  \__, |\___|
                                                                          |___/      
 _          _     _                   
| |   _   _| |__ (_) __ _ _ __   __ _ 
| |  | | | | '_ \| |/ _` | '_ \ / _` |
| |__| |_| | |_) | | (_| | | | | (_| |
|_____\__,_|_.__/|_|\__,_|_| |_|\__,_|              

                                                                                       
                                                                                        

----------------------------------------------------------------------------------------
          \n \n""")

def print_data():
    nom = print_nom()
    prenom = print_prenom()
    date_naissance = print_birth()

    if nom.strip() and prenom.strip() and date_naissance.strip():
        print(f"\nNom : {nom}\nPrénom : {prenom}\nDate de naissance : {date_naissance}")
    else:
        print("La carte doit être attribuée pour en voir les données.")

def assign_card():
    global is_card_assigned

    nom = intro_nom()
    prenom = intro_prenom()
    birth = intro_birth()

    if nom is None or prenom is None or birth is None:
        print("Erreur : les informations n'ont pas été correctement saisies ou une erreur de transmission est survenue.")
    else:
        is_card_assigned = True
        
#Modification du menu
def print_menu():
    print (" 1 - Afficher la version de carte ")
    print (" 2 - Afficher les données de la carte ")
    print (" 3 - Attribuer la carte ")
    print (" 4 - Mettre le solde initial ")
    print (" 5 - Consulter le solde ")
    print (" 6 - Quitter ")


#Partie main


def main():
    init_smart_card()
    print_hello_message()
    while True:
        print_menu()
        cmd = int(input("Choix : "))
        if (cmd == 1):
            print_version()
        elif (cmd == 2):
        	print_data()
        elif (cmd == 3):
        	assign_card()
        elif (cmd == 4):
            recharge_card()
        elif (cmd == 5):
            get_balance()
        elif (cmd == 6):
            return
        else:
            print("Commande inconnue !")
        print("\n ---\n")


if __name__ == '__main__':
	main()
