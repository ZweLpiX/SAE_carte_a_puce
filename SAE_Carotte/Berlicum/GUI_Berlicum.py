import tkinter as tk
import tkinter.simpledialog as sd
import smartcard.System as scardsys
import smartcard.util as scardutil
import smartcard.Exceptions as scardexcp
import mysql.connector
import tkinter.messagebox as messagebox

db_config = {
    'user': 'berlicum',
    'password': 'root',
    'host': '192.168.56.102',
    'database': 'purpledragon',
}

def test_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        print("Connexion réussie à la base de données")
        connection.close()
    except mysql.connector.Error as err:
        print("Erreur lors de la connexion à la base de données:", err)

# Appeler cette fonction pour tester la connexion
test_db_connection()

# Variable globale pour la connexion à la carte
global conn_reader
conn_reader = None

def init_smart_card():
    global conn_reader
    try:
        lst_readers = scardsys.readers()
        if len(lst_readers) < 1:
            return "Pas de lecteur de carte connecté !"
        conn_reader = lst_readers[0].createConnection()
        conn_reader.connect()
        return "Connexion au lecteur de carte établie."
    except scardexcp.Exceptions as e:
        return str(e)
        
       
def create_gui():
    global conn_reader
    init_message = init_smart_card()  # Initialisez conn_reader ici
    if init_message != "Connexion au lecteur de carte établie.":
        print(init_message)
        return  # Arrêtez l'exécution si la connexion échoue

    root = tk.Tk()
    root.title("Berlicum Control Panel")
    status_label = tk.Label(root, text="En attente d'une action...", fg="blue")
    status_label.pack()
    
    
# Autres fonctions (get_student_info_from_db, get_nom, get_prenom, etc.)
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

def get_total_bonus(nom, prenom):
    student_bonus_info = get_student_info_from_db(nom, prenom)
    total_bonus = sum(montant for _, montant, _ in student_bonus_info)
    return total_bonus
   
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
# Fonctions adaptées pour l'interface graphique

def gui_verify_student_info(status_label):
    global conn_reader
    if conn_reader is None:
        status_label.config(text="Lecteur de carte non initialisé.")
        return
    nom = get_nom()
    prenom = get_prenom()
    student_bonus_info = get_student_info_from_db(nom, prenom)
    
    if student_bonus_info:
        info = "Vrai : L'étudiant est présent dans la base de données.\nBonus attribués à l'étudiant :\n"
        for _, montant, libelle in student_bonus_info:
            info += f"Montant: {montant}, Libellé: {libelle}\n"
        status_label.config(text=info)
    else:
        status_label.config(text="Faux : L'étudiant n'est pas trouvé dans la base de données.")

def gui_get_balance(status_label):
    # APDU pour lire le solde de la carte
    apdu = [0x82, 0x01, 0x00, 0x00, 0x02]
    try:
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
            status_label.config(text=f"Solde : {balance} €")
        except ValueError:
            status_label.config(text="Erreur de conversion du solde en nombre.")

    except smartcard.Exceptions.CardConnectionException as e:
        status_label.config(text=f"Erreur de connexion à la carte : {e}")

def gui_calculate_total_balance(status_label):
    try:
        nom = get_nom()
        prenom = get_prenom()
        total_bonus = get_total_bonus(nom, prenom)
        current_balance = get_balance()
        total_bonus = float(total_bonus)
        total_balance = total_bonus + current_balance

        # Mettre à jour le solde sur la carte
        recharge_card(total_balance)
        delete_student_account_entries(nom, prenom)

        status_label.config(text=f"Total (Solde + Bonus) : {total_balance} €")
    except Exception as e:
        status_label.config(text=f"Erreur : {e}")


def gui_recharge_with_bank_card(status_label):
    # Demande d'insérer la carte bancaire
    messagebox.showinfo("Information", "Veuillez insérer votre carte bancaire...")

    # Demande du montant à recharger
    montant_str = sd.askstring("Montant de recharge", "Entrez le montant à recharger sur la carte :")
    if not montant_str:
        status_label.config(text="Opération annulée.")
        return

    try:
        montant = float(montant_str)
    except ValueError:
        status_label.config(text="Entrée invalide. Opération annulée.")
        return

    # Simulation de transaction bancaire
    status_label.config(text="Traitement de la transaction bancaire...")
    # Ici, vous pouvez implémenter une simulation de transaction

    # Mise à jour du solde sur la carte de l'étudiant
    try:
        current_balance = get_balance()
        new_balance = current_balance + montant
        recharge_card(new_balance)
        status_label.config(text=f"Transaction réussie. Votre compte a été crédité de {montant:.2f}€.")
    except Exception as e:
        status_label.config(text=f"Erreur lors de la recharge : {e}")


# Interface graphique principale
def create_gui():
    global conn_reader
    init_message = init_smart_card()
    if conn_reader is None:
        print(init_message)
        return
        
button_color = "#4a7abc"  # Bleu
button_text_color = "white"
button_font = ("Helvetica", 12)

def create_gui():
    global conn_reader
    init_message = init_smart_card()
    if conn_reader is None:
        print(init_message)
        return
        
    root = tk.Tk()
    root.title("Berlicum Control Panel")

    main_frame = tk.Frame(root, bg='light gray')
    main_frame.pack(padx=10, pady=10)

    status_label = tk.Label(main_frame, text="En attente d'une action...", fg="blue", bg='light gray', font=("Helvetica", 12))
    status_label.pack()

    # Boutons avec des couleurs et des polices personnalisées
    button_info = tk.Button(main_frame, text="Afficher mes bonus", command=lambda: gui_verify_student_info(status_label), bg=button_color, fg=button_text_color, font=button_font)
    button_info.pack(fill=tk.X, pady=5)

    button_balance = tk.Button(main_frame, text="Afficher le solde actuel sur la carte", command=lambda: gui_get_balance(status_label), bg=button_color, fg=button_text_color, font=button_font)
    button_balance.pack(fill=tk.X, pady=5)

    button_total_balance = tk.Button(main_frame, text="Convertir les bonus", command=lambda: gui_calculate_total_balance(status_label), bg=button_color, fg=button_text_color, font=button_font)
    button_total_balance.pack(fill=tk.X, pady=5)

    button_recharge = tk.Button(main_frame, text="Recharger avec ma carte bancaire", command=lambda: gui_recharge_with_bank_card(status_label), bg=button_color, fg=button_text_color, font=button_font)
    button_recharge.pack(fill=tk.X, pady=5)

    # Ajoutez d'autres boutons et fonctionnalités selon vos besoins

    root.mainloop()

if __name__ == '__main__':
    create_gui()
    
    
    
    

