import tkinter as tk
import re
from datetime import datetime
import tkinter.simpledialog as sd
from smartcard.System import readers
from smartcard.Exceptions import CardConnectionException

# Variables globales
global conn_reader
conn_reader = None

def init_smart_card():
    global conn_reader
    try:
        card_readers = readers()
        if not card_readers:
            return "Aucun lecteur de carte détecté."
        conn_reader = card_readers[0].createConnection()
        conn_reader.connect()
        return "Connexion au lecteur de carte établie."
    except Exception as e:
        return "Erreur d'initialisation : " + str(e)
# Initialisation automatique du lecteur de carte
init_message = init_smart_card()


global is_card_assigned
is_card_assigned = False
        
def is_valid_date(date_str):
    """ Vérifie si la date est valide et dans la plage spécifiée. """
    try:
        date_obj = datetime.strptime(date_str, '%d%m%Y')
        return 1950 <= date_obj.year <= 2010
    except ValueError:
        return False
        
def print_version(status_label):
    global conn_reader
    if not conn_reader:
        status_label.config(text="Lecteur de carte non initialisé.")
        return

    try:
        apdu = [0x81, 0x00, 0x00, 0x00, 0x04]  # Instruction à transmettre à la carte
        data, sw1, sw2 = conn_reader.transmit(apdu)
        if sw1 != 0x90 or sw2 != 0x00:
            status_label.config(text="Erreur de lecture de la version de la carte.")
            return

        version_str = ''.join(chr(e) for e in data)
        status_label.config(text=f"Version de la carte : {version_str}")

    except CardConnectionException as e:
        status_label.config(text="Erreur de connexion à la carte : " + str(e))

def print_data(status_label):
    nom = print_nom()
    prenom = print_prenom()
    date_naissance = print_birth()
    status_label.config(text=f"Nom: {nom}, Prénom: {prenom}, Date de naissance: {date_naissance}")

def print_nom():
    global conn_reader
    try:
        apdu = [0x81, 0x02, 0x00, 0x00, 0x00]
        data, sw1, sw2 = conn_reader.transmit(apdu)
        apdu[4] = sw2
        data, sw1, sw2 = conn_reader.transmit(apdu)
        nom = ''.join(chr(e) for e in data)
        return nom
    except CardConnectionException:
        return "Erreur lors de la lecture du nom."

def print_prenom():
    global conn_reader
    try:
        apdu = [0x81, 0x04, 0x00, 0x00, 0x00]
        data, sw1, sw2 = conn_reader.transmit(apdu)
        apdu[4] = sw2
        data, sw1, sw2 = conn_reader.transmit(apdu)
        prenom = ''.join(chr(e) for e in data)
        return prenom
    except CardConnectionException:
        return "Erreur lors de la lecture du prénom."

def print_birth():
    global conn_reader
    try:
        apdu = [0x81, 0x06, 0x00, 0x00, 0x00]
        data, sw1, sw2 = conn_reader.transmit(apdu)
        apdu[4] = sw2
        data, sw1, sw2 = conn_reader.transmit(apdu)
        birth = ''.join(chr(e) for e in data)
        return birth
    except CardConnectionException:
        return "Erreur lors de la lecture de la date de naissance."

def is_valid_name(name):
    """ Vérifie si le nom/prénom est valide. """
    return re.match(r'^[A-Z][a-zA-Z]{0,9}$', name) is not None

def intro_nom():
    global conn_reader
    while True:
        nom = sd.askstring("Nom de l'élève", "Saisissez le Nom de l'élève :")
        if nom is None:
            return "Action annulée."
        if is_valid_name(nom):
            apdu = [0x81, 0x01, 0x00, 0x00, len(nom)] + [ord(c) for c in nom]
            try:
                conn_reader.transmit(apdu)
                return f"Nom attribué : {nom}"
            except CardConnectionException as e:
                return "Erreur : " + str(e)
        else:
            tk.messagebox.showerror("Erreur", "Nom invalide. Veuillez entrer un nom correct.")

def intro_prenom():
    global conn_reader
    while True:
        prenom = sd.askstring("Prénom de l'élève", "Saisissez le Prénom de l'élève :")
        if prenom is None:
            return "Annulé"
        if not is_valid_name(prenom):
            tk.messagebox.showerror("Erreur", "Prénom invalide. Veuillez entrer un prénom correct.")
            continue
        apdu = [0x81, 0x03, 0x00, 0x00, len(prenom)] + [ord(c) for c in prenom]
        try:
            conn_reader.transmit(apdu)
            return f"Prénom attribué : {prenom}"
        except CardConnectionException as e:
            return "Erreur : " + str(e)

def is_valid_date(date_str):
    """ Vérifie si la date est valide et dans la plage spécifiée. """
    try:
        date_obj = datetime.strptime(date_str, '%d%m%Y')
        return 1 <= date_obj.day <= 31 and 1 <= date_obj.month <= 12 and 1950 <= date_obj.year <= 2010
    except ValueError:
        return False

def intro_birth():
    global conn_reader
    while True:
        birth = sd.askstring("Date de naissance", "Saisissez la date de naissance (Format : JJMMAAAA) :")
        if not birth:
            return "Annulé"
        if not is_valid_date(birth):
            tk.messagebox.showerror("Erreur", "Date invalide. Veuillez saisir une date cohérente.")
            continue

        apdu = [0x81, 0x05, 0x00, 0x00, len(birth)] + [ord(c) for c in birth]
        try:
            conn_reader.transmit(apdu)
            return f"Date de naissance attribuée : {birth[:2]}/{birth[2:4]}/{birth[4:]}"
        except CardConnectionException as e:
            return "Erreur : " + str(e)

def assign_card(status_label):
    global is_card_assigned
    status_nom = intro_nom()
    status_prenom = intro_prenom()
    status_birth = intro_birth()
    status_label.config(text=f"{status_nom}, {status_prenom}, {status_birth}")
    if "Nom attribué" in status_nom and "Prénom attribué" in status_prenom and "Date de naissance attribuée" in status_birth:
        is_card_assigned = True

def recharge_card(status_label):
    global conn_reader
    solde = '1.00'

    try:
        apdu = [0x82, 0x02, 0x00, 0x00, len(solde)] + [ord(c) for c in solde]
        sw1, sw2 = conn_reader.transmit(apdu)[1:3]
        if sw1 == 0x90:
            status_label.config(text=f"La carte a été créditée avec succès de {solde}€.")
        else:
            status_label.config(text=f"Erreur lors du rechargement : SW1=0x{sw1:02X}, SW2=0x{sw2:02X}")
    except CardConnectionException as e:
        status_label.config(text="Erreur de connexion : " + str(e))


def get_balance():
    global conn_reader
    try:
        apdu = [0x82, 0x01, 0x00, 0x00, 0x02]
        data, sw1, sw2 = conn_reader.transmit(apdu)
        apdu[4] = sw2
        data, sw1, sw2 = conn_reader.transmit(apdu)
        balance_str = ''.join(chr(e) for e in data)
        return f"Solde : {balance_str} €"
    except CardConnectionException:
        return "Erreur lors de la lecture du solde."

def show_balance(status_label):
    balance = get_balance()
    status_label.config(text=balance)
    
  
# Interface graphique
root = tk.Tk()
root.title("Lubiana Control Panel")

main_frame = tk.Frame(root, bg='light gray')
main_frame.pack(padx=10, pady=10)

status_label = tk.Label(main_frame, text="En attente d'une action...", fg="blue", bg='light gray', font=("Helvetica", 12))
status_label.pack()

# Boutons avec des couleurs et des polices personnalisées
button_font = ("Helvetica", 12)
button_color = "#4a7abc"

version_button = tk.Button(main_frame, text="Afficher la version", command=lambda: print_version(status_label), bg=button_color, fg='white', font=button_font)
version_button.pack(fill=tk.X, pady=5)

data_button = tk.Button(main_frame, text="Afficher les données", command=lambda: print_data(status_label), bg=button_color, fg='white', font=button_font)
data_button.pack(fill=tk.X, pady=5)

assign_button = tk.Button(main_frame, text="Attribuer la carte", command=lambda: assign_card(status_label), bg=button_color, fg='white', font=button_font)
assign_button.pack(fill=tk.X, pady=5)

recharge_button = tk.Button(main_frame, text="Recharger 1€ sur la carte", command=lambda: recharge_card(status_label), bg=button_color, fg='white', font=button_font)
recharge_button.pack(fill=tk.X, pady=5)

balance_button = tk.Button(main_frame, text="Consulter le solde", command=lambda: show_balance(status_label), bg=button_color, fg='white', font=button_font)
balance_button.pack(fill=tk.X, pady=5)

root.mainloop()
