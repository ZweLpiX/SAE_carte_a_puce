# Importation des librairies 

import smartcard.System as scardsys
import smartcard.util as scardutil
import smartcard.Exceptions as scardexcp


import mysql.connector

db_config = {
    'user': 'berlicum',  # L'utilisateur ayant les privilèges
    'password': 'root',  # Le mot de passe que vous avez indiqué pour 'berlicum'
    'host': '192.168.56.102',  # L'adresse IP du serveur MySQL distant
    'database': 'purpledragon',
}

def get_student_info_from_db(nom, prenom):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = """
    SELECT etudiant.etu_id, compte.opr_montant, compte.opr_libelle 
    FROM etudiant 
    JOIN compte ON etudiant.etu_id = compte.etu_id 
    WHERE etudiant.etu_nom = %s AND etudiant.etu_prenom = %s AND compte.type_operation = 'Bonus'
    """
    cursor.execute(query, (nom, prenom))
    results = cursor.fetchall()  # Utilisez fetchall pour obtenir tous les bonus correspondants
    cursor.close()
    connection.close()
    return results  # Renvoie une liste de tuples contenant les infos des bonus

def get_nom():
    apdu = [0x81, 0x02, 0x00, 0x00, 0x00] # Instruction to send to the card
    data, sw1, sw2 = conn_reader.transmit(apdu) # Send the command to the card and get the data, along with the SW1 and SW2 codes in return
    apdu[4] = sw2 # Update the fifth byte of the instruction to correspond to the SW2 byte
    data, sw1, sw2 = conn_reader.transmit(apdu) # Resend the command and get its data
    nom = "" # This will store the name extracted from the card
    for e in data:
        nom += chr(e)
    return nom

def get_prenom():
    apdu = [0x81, 0x04, 0x00, 0x00, 0x00] # Instruction to send to the card
    data, sw1, sw2 = conn_reader.transmit(apdu) # Send the command to the card and get the data, along with the SW1 and SW2 codes in return
    apdu[4] = sw2 # Update the fifth byte of the instruction to correspond to the SW2 byte
    data, sw1, sw2 = conn_reader.transmit(apdu) # Resend the command and get its data
    prenom = "" # This will store the first name extracted from the card
    for e in data:
        prenom += chr(e)
    return prenom

def verify_student_info():
    nom = get_nom()
    prenom = get_prenom()
    student_bonus_info = get_student_info_from_db(nom, prenom)
    
    if student_bonus_info:
        print("Vrai : L'étudiant est présent dans la base de données.")
        print("Bonus attribués à l'étudiant :")
        for _, montant, libelle in student_bonus_info:
            # Supprimez l'affichage de l'ID et affichez uniquement le montant et le libellé
            print(f"Montant: {montant}, Libellé: {libelle}")
    else:
        print("Faux : L'étudiant n'est pas trouvé dans la base de données.")


#Fonction permettant de récuperer le solde de la carte
def get_balance():
    # APDU pour lire le solde de la carte
    apdu = [0x82, 0x01, 0x00, 0x00, 0x02]
    data, sw1, sw2 = conn_reader.transmit(apdu)
    apdu[4] = sw2
    data, sw1, sw2 = conn_reader.transmit(apdu)

    balance_str = ""
    for e in data:
        balance_str += chr(e)

    # Nettoyer la chaîne pour ne garder que les chiffres et le point
    balance_str = ''.join(filter(lambda x: x.isdigit() or x == '.', balance_str))

    try:
        # Convertir en nombre décimal
        balance = float(balance_str)
    except ValueError:
        print("Erreur de conversion du solde en nombre.")
        balance = 0.0  # Retourner 0.0 en cas d'erreur

    print(f"Solde : {balance} €")
    return balance

    
# Ajoutez cette nouvelle fonction
def calculate_total_balance():
    nom = get_nom()
    prenom = get_prenom()
    total_bonus = get_total_bonus(nom, prenom)
    current_balance = get_balance()
    total_bonus = float(total_bonus)
    total_balance = total_bonus + current_balance
    print(f"Total (Solde + Bonus) : {total_balance} €")

    # Mettre à jour le solde sur la carte
    recharge_card(total_balance)
    delete_student_account_entries(nom, prenom)
    
def get_total_bonus(nom, prenom):
    student_bonus_info = get_student_info_from_db(nom, prenom)
    total_bonus = sum(montant for _, montant, _ in student_bonus_info)
    return total_bonus
    
    
def recharge_card(new_balance):
    solde_str = f"{new_balance:.2f}"  # Convertir le nouveau solde en chaîne de caractères

    apdu = [0x82, 0x02, 0x00, 0x00, len(solde_str)]  # Longueur du solde en tant que dernière partie de l'APDU
    for e in solde_str:
        apdu.append(ord(e))

    try:
        data, sw1, sw2 = conn_reader.transmit(apdu)
        if sw1 == 0x90:
            print(f"La carte a été mise à jour avec succès. Nouveau solde : {solde_str}€.")
        else:
            print(f"Erreur lors de la mise à jour de la carte : SW1=0x{sw1:02X}, SW2=0x{sw2:02X}")
    except scardexcp.CardConnectionException as e:
        print("Erreur : ", e)

def delete_student_account_entries(nom, prenom):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query_etu_id = "SELECT etu_id FROM etudiant WHERE etu_nom = %s AND etu_prenom = %s"
    cursor.execute(query_etu_id, (nom, prenom))
    etu_id_result = cursor.fetchone()
    if etu_id_result:
        etu_id = etu_id_result[0]
        delete_query = "DELETE FROM compte WHERE etu_id = %s"
        cursor.execute(delete_query, (etu_id,))
        connection.commit()
        print(f"Toutes les entrées de compte pour l'étudiant {nom} {prenom} ont été supprimées.")
    else:
        print("Aucun étudiant trouvé avec ce nom et prénom.")
    cursor.close()
    connection.close()

def recharge_with_bank_card():
    print("Veuillez insérer votre carte bancaire...")
    input("Appuyez sur une touche pour continuer une fois que la carte est insérée.")
    
    try:
        montant = float(input("Entrez le montant à recharger sur la carte : "))
    except ValueError:
        print("Entrée invalide. Opération annulée.")
        return

    # Vous pouvez ajouter ici une simulation de transaction bancaire
    print("Traitement de la transaction bancaire...")
    print("Transaction réussie. Votre compte a été crédité de {:.2f}€.".format(montant))

    # Mise à jour du solde sur la carte de l'étudiant
    current_balance = get_balance()
    new_balance = current_balance + montant
    recharge_card(new_balance)


############################################################################################################################################################

#Partie Smart Card

#Modification de la fonction init_smart_card

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

    #Stockez l'ATR dans une variable globale
    global card_atr
    card_atr = atr

    return
    
############################################################################################################################################################
    
def print_nom():
    apdu = [0x81, 0x02, 0x00, 0x00, 0x00] # Instruction à transmettre à la carte
    data, sw1, sw2 = conn_reader.transmit(apdu) # Envoyer la commande à la carte et récupérer les données, ainsi que les codes SW1 et SW2 en retour
    apdu[4] = sw2 # Met à jour le cinquième octet de l'instruction qui correspond à l'octet SW2
    data, sw1, sw2 = conn_reader.transmit(apdu) # On renvoie la commande et on récupère ses données
    str = ""
    for e in data:
        str += chr(e)
    print ("""
        Nom : %s""" % (str))    
    return

#Fonction affichant le prénom de l'utilisateur de la carte
def print_prenom():
    apdu = [0x81, 0x04, 0x00, 0x00, 0x00] # Instruction à transmettre à la carte
    data, sw1, sw2 = conn_reader.transmit(apdu) # Envoyer la commande à la carte et récupérer les données, ainsi que les codes SW1 et SW2 en retour
    apdu[4] = sw2 # Met à jour le cinquième octet de l'instruction qui correspond à l'octet SW2
    data, sw1, sw2 = conn_reader.transmit(apdu) # On renvoie la commande et on récupère ses données
    str = ""
    for e in data:
        str += chr(e)
    print ("""
        Prénom : %s""" % (str))    
    return

#Fonction affichant la date de naissance de l'utilisateur de la carte
def print_birth():
    apdu = [0x81, 0x06, 0x00, 0x00, 0x00] # Instruction à transmettre à la carte
    data, sw1, sw2 = conn_reader.transmit(apdu) # Envoyer la commande à la carte et récupérer les données, ainsi que les codes SW1 et SW2 en retour
    apdu[4] = sw2 # Met à jour le cinquième octet de l'instruction qui correspond à l'octet SW2
    data, sw1, sw2 = conn_reader.transmit(apdu) # On renvoie la commande et on récupère ses données
    str = ""
    for e in data:
        str += chr(e)
    print ("""
        Date de naissance : %s""" % (str))    
    return
    
 ############################################################################################################################################################
    
    #Création du menu


#Modification du message de bienvenue
def print_hello_message():
    print("""

BERLICUM - Welcome                                                                                     
                                                                                    
----------------------------------------------------------------------------------------
          \n \n""")

def print_data():
    print_nom()
    print_prenom()
    print_birth()

def assign_card():
    intro_nom()
    intro_prenom()
    intro_birth()

#Modification du menu
def print_menu():
    print(" 1 - Afficher mes informations")
    print(" 2 - Vérifier l'information de l'étudiant")
    print(" 3 - Afficher le solde actuel sur la carte")
    print(" 4 - Calculer le total (Solde + Bonus)")
    print(" 5 - Recharger avec ma carte bancaire")
    print(" 6 - Quitter")

def main():
    init_smart_card()
    print_hello_message()
    while True:
        print_menu()
        cmd = int(input("Choix : "))
        if cmd == 1:
            print_data()
        elif cmd == 2:
            verify_student_info()
        elif cmd == 3:
            get_balance()
        elif cmd == 4:
            calculate_total_balance()  # Nouvelle fonction pour calculer le total
        elif cmd == 5:
            recharge_with_bank_card()
        elif cmd == 6:
            return
        else:
            print("Commande inconnue !")
        print("\n ---\n")

if __name__ == '__main__':
    main()
