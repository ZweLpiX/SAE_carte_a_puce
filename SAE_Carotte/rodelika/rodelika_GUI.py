import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Entry, Button
import mysql.connector
from datetime import datetime

# Connexion à la base de données
cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='purpledragon')

def get_list_students():
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT etudiant.etu_id, etudiant.etu_nom, etudiant.etu_prenom FROM etudiant")
    students = cursor.fetchall()
    cursor.close()
    return students

def get_total_balance():
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT etudiant.etu_id, etudiant.etu_nom, etudiant.etu_prenom, IFNULL(SUM(compte.opr_montant), 0) as total FROM etudiant LEFT JOIN compte ON etudiant.etu_id = compte.etu_id GROUP BY etudiant.etu_id")
    balances = cursor.fetchall()
    cursor.close()
    return balances

def insert_new_student(nom, prenom):
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO etudiant (etu_nom, etu_prenom) VALUES (%s, %s)", (nom, prenom))
    cnx.commit()
    cursor.close()

def assign_bonus(etu_id, commentaire, montant):
    cursor = cnx.cursor()
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO compte (etu_id, opr_date, opr_montant, opr_libelle, type_operation) VALUES (%s, %s, %s, %s, 'Bonus')", (etu_id, current_datetime, montant, commentaire))
    cnx.commit()
    cursor.close()

# Fonctions pour l'interface graphique
def list_students():
    students = get_list_students()
    student_info = "\n".join([f"ID: {student['etu_id']}, Nom: {student['etu_nom']}, Prénom: {student['etu_prenom']}" for student in students])
    messagebox.showinfo("Liste des étudiants", student_info)

def student_balances():
    balances = get_total_balance()
    balance_info = "\n".join([f"{balance['etu_nom']} {balance['etu_prenom']} : {balance['total']}€" for balance in balances])
    messagebox.showinfo("Solde des étudiants", balance_info)

def new_student():
    def submit():
        nom = nom_entry.get()
        prenom = prenom_entry.get()
        insert_new_student(nom, prenom)
        messagebox.showinfo("Nouvel étudiant", f"Étudiant {nom} {prenom} a été créé avec succès.")
        popup.destroy()

    popup = Toplevel(root)
    popup.title("Nouvel étudiant")

    Label(popup, text="Nom:").pack()
    nom_entry = Entry(popup)
    nom_entry.pack()

    Label(popup, text="Prénom:").pack()
    prenom_entry = Entry(popup)
    prenom_entry.pack()

    submit_button = Button(popup, text="Créer", command=submit)
    submit_button.pack()

def assign_bonus_gui():
    etu_id = simpledialog.askstring("ID Étudiant", "Entrez l'ID de l'étudiant:")
    montant = simpledialog.askstring("Montant", "Entrez le montant du bonus:")
    commentaire = simpledialog.askstring("Commentaire", "Entrez un commentaire:")
    assign_bonus(etu_id, commentaire, montant)
    messagebox.showinfo("Bonus", f"Bonus de {montant} euros attribué à l'étudiant {etu_id}.")

def show_credits():
    messagebox.showinfo("Crédits", "Logiciel SAE.\n Nabil, Clément, Maxime, Nicolas !" )

# Création de l'interface graphique
root = tk.Tk()
root.title("Rodelika - Logiciel de gestion")

tk.Button(root, text="Liste des étudiants", command=list_students).pack()
tk.Button(root, text="Solde des étudiants", command=student_balances).pack()
tk.Button(root, text="Saisir un nouvel étudiant", command=new_student).pack()
tk.Button(root, text="Attribuer un bonus", command=assign_bonus_gui).pack()
tk.Button(root, text="Crédits", command=show_credits).pack()
tk.Button(root, text="Quitter", command=root.quit).pack()

root.mainloop()
