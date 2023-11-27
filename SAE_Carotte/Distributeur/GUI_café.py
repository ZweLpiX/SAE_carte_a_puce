import tkinter as tk
import tkinter.simpledialog as sd
import smartcard.System as scardsys
import smartcard.util as scardutil
import smartcard.Exceptions as scardexcp
import tkinter.messagebox as messagebox

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

def gui_payement(status_label):
    global conn_reader
    if conn_reader is None:
        status_label.config(text="Lecteur de carte non initialisé.")
        return

    try:
        # Lecture du solde actuel
        apdu = [0x82, 0x01, 0x00, 0x00, 0x02]
        data, sw1, sw2 = conn_reader.transmit(apdu)
        apdu[4] = sw2
        data, sw1, sw2 = conn_reader.transmit(apdu)

        solde_str = ''.join(chr(e) for e in data if chr(e).isdigit() or chr(e) in ['.', '-'])
        solde = float(solde_str)
        
        # Déduction du prix de la boisson
        prix_boisson = 0.20
        nouveau_solde = solde - prix_boisson

        # Préparation de la commande APDU pour la mise à jour du solde
        nouveau_solde_str = f"{nouveau_solde:.2f}"
        apdu = [0x82, 0x02, 0x00, 0x00, len(nouveau_solde_str)] + [ord(c) for c in nouveau_solde_str]
        
        data, sw1, sw2 = conn_reader.transmit(apdu)
        if sw1 == 0x90:
            status_label.config(text=f"La carte a été débitée de 0.20€. Nouveau solde: {nouveau_solde:.2f}€")
        else:
            status_label.config(text=f"Erreur lors du débit : SW1=0x{sw1:02X}, SW2=0x{sw2:02X}")
    
    except scardexcp.CardConnectionException as e:
        status_label.config(text="Erreur : " + str(e))



    # Logique de paiement ici, mettez à jour status_label avec le résultat

# Interface graphique principale
def create_gui():
    global conn_reader
    init_message = init_smart_card()
    if conn_reader is None:
        print(init_message)
        return
        
    root = tk.Tk()
    root.title("Café Control Panel")

    main_frame = tk.Frame(root, bg='light gray')
    main_frame.pack(padx=10, pady=10)

    status_label = tk.Label(main_frame, text="Bienvenue à la machine", fg="blue", bg='light gray', font=("Helvetica", 12))
    status_label.pack()

    # Définition des couleurs et des styles pour les boutons
    button_color = "#4a7abc"  # Bleu
    button_text_color = "white"
    button_font = ("Helvetica", 12)

    # Boutons avec des couleurs et des polices personnalisées
    button_cafe = tk.Button(main_frame, text="Café (0.20 €)", command=lambda: gui_payement(status_label), bg=button_color, fg=button_text_color, font=button_font)
    button_cafe.pack(fill=tk.X, pady=5)

    button_the = tk.Button(main_frame, text="Thé (0.20 €)", command=lambda: gui_payement(status_label), bg=button_color, fg=button_text_color, font=button_font)
    button_the.pack(fill=tk.X, pady=5)

    button_chocolat = tk.Button(main_frame, text="Chocolat Chaud (0.20 €)", command=lambda: gui_payement(status_label), bg=button_color, fg=button_text_color, font=button_font)
    button_chocolat.pack(fill=tk.X, pady=5)

    button_quit = tk.Button(main_frame, text="Quitter", command=root.destroy, bg=button_color, fg=button_text_color, font=button_font)
    button_quit.pack(fill=tk.X, pady=5)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
