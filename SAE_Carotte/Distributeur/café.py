# Importation des librairies 

import smartcard.System as scardsys
import smartcard.util as scardutil
import smartcard.Exceptions as scardexcp
import time

#Partie Smart Card

# Modification de la fonction init_smart_card

def init_smart_card():
    try:
        lst_readers = scardsys.readers()
    except scardexcp.Exceptions as e:
        print(e)
        return

    if len(lst_readers) < 1:
        print("Pas de lecteur de carte connecté !")
        exit()

    global conn_reader
    conn_reader = lst_readers[0].createConnection()

    try:
        conn_reader.connect()
    except Exception as e:
        if 'Card is unpowered' in str(e):
            print("Pas de carte dans le lecteur : ", e)
            exit()
        else:
            print("Erreur de connexion au lecteur de carte : ", e)
            exit()

    atr = conn_reader.getATR()

    # Stockez l'ATR dans une variable globale
    global card_atr
    card_atr = atr

    return


#Créations des fonctions différentes 

#Fonction permettant de procéder au payement de la boisson

def payement():
    apdu = [0x82, 0x01, 0x00, 0x00, 0x02]  # Commande pour la lecture du solde
    data, sw1, sw2 = conn_reader.transmit(apdu)  # Envoi de la commande à la carte
    apdu[4] = sw2 # Met à jour le cinquième octet de l'instruction qui correspond à l'octet SW2
    data, sw1, sw2 = conn_reader.transmit(apdu) # On renvoie la commande et on récupère ses données
    string_vide = ""
    for e in data:
        string_vide += chr(e)
    solde = ''.join(char for char in string_vide if char.isdigit() or char in ['.', '-']) #Supprime tous les caractères de la chaîne qui ne sont pas des chiffres,
    solde = float(solde)                                                                  #des points décimaux ou des signes négatifs
    temp = solde - 0.20                                                                   #Ensuite, il essaie de convertir la chaîne nettoyée en float
    temp = "%.2f" %temp
    nv_solde = str(temp)
    
        # Introduisez un délai ici
    print("Traitement du paiement en cours...")
    time.sleep(5)  # Définissez ici la durée du délai en secondes
    
    apdu = [0x82, 0x02, 0x00, 0x00, 0x05]  # Commande pour créditer la carte
    length_solde = len(nv_solde)
    apdu.append(length_solde)
    for e in nv_solde:
        apdu.append(ord(e))
    try:
        data, sw1, sw2 = conn_reader.transmit(apdu)  # Envoi de la commande à la carte
        if sw1 == 0x90:  # Si la commande s'est exécutée avec succès
            print(f"""
                  La carte a été débiter avec succès de 0.20€. \t
                  Montant restant: {nv_solde}""")
        else:
            print(f"Erreur lors du rechargement de la carte : SW1=0x{sw1:02X}, SW2=0x{sw2:02X}")
    except scardexcp.CardConnectionException as e:
        print("Erreur : ", e)
    return


#Création du menu


#Modification du message de bienvenue
def print_hello_message():
    print("""

     __  __            _     _                    
    |  \/  | __ _  ___| |__ (_)_ __   ___    __ _ 
    | |\/| |/ _` |/ __| '_ \| | '_ \ / _ \  / _` |
    | |  | | (_| | (__| | | | | | | |  __/ | (_| |
    |_|  |_|\__,_|\___|_| |_|_|_| |_|\___|  \__,_|

      ____       __      
     / ___|__ _ / _| ___ 
    | |   / _` | |_ / _ \ \t
    | |__| (_| |  _|  __/
     \____\__,_|_|  \___|     
    ---------------------------------------------------
              \n \n""")

def print_menu():
    print("-- PRIX DES BOISSONS: 0.20 € --")
    print("1 - Café")
    print("2 - Thé")
    print("3 - Chocolat Chaud")
    print("4 - Quitter")



def main():
    init_smart_card()
    print_hello_message()
    while True:
        print_menu()
        cmd = int(input("Choix : "))
        if (cmd == 1):
            payement()
        elif (cmd == 2):
            payement()
        elif (cmd == 3):
            payement()
        elif (cmd == 4):
            return



if __name__ == '__main__':
    main()
