import mysql.connector
from decimal import Decimal
from datetime import datetime

cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='purpledragon')

def print_hello_message():
    print("-----------------------------------")
    print("-- Logiciel de gestion : Rodlika --")
    print("-----------------------------------")

def print_menu():
    print("1 - Afficher la liste des étudiants")
    print("2 - Afficher le solde des étudiants")
    print("3 - Saisir un nouvel étudiant")
    print("4 - Attribuer un bonus")
    print("5 - Quitter")

def get_list_students():
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("""
        SELECT etudiant.etu_id, etudiant.etu_nom, etudiant.etu_prenom,
               IFNULL(SUM(compte.opr_montant), 0) as total, GROUP_CONCAT(compte.opr_libelle SEPARATOR ', ') as commentaires
        FROM etudiant
        LEFT JOIN compte ON etudiant.etu_id = compte.etu_id
        GROUP BY etudiant.etu_id
    """)
    students = cursor.fetchall()
    cursor.close()
    return students

def display_students():
    students = get_list_students()
    for student in students:
        print(f"ID: {student['etu_id']}, Nom: {student['etu_nom']}, Prénom: {student['etu_prenom']}, Solde: {student['total']}, Commentaires: {student['commentaires']}")

def get_total_balance():
    cursor = cnx.cursor()
    cursor.execute("SELECT etudiant.etu_id, etudiant.etu_nom, etudiant.etu_prenom, IFNULL(SUM(compte.opr_montant), 0) as total FROM etudiant LEFT JOIN compte ON etudiant.etu_id = compte.etu_id GROUP BY etudiant.etu_id")
    balances = cursor.fetchall()
    cursor.close()
    return balances

def display_balances():
    balances = get_total_balance()
    for balance in balances:
        print(balance)

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
    
    print(f"Bonus de {montant} euros attribué à l'étudiant {etu_id}.")

def main():
    print_hello_message()
 
    while True:
        print_menu()
        choix = input("Choix : ")

        if choix == '1':
            display_students()
        elif choix == '2':
            display_balances()
        elif choix == '3':
            nom = input("Nom de l'étudiant : ")
            prenom = input("Prénom de l'étudiant : ")
            insert_new_student(nom, prenom)
            print("Étudiant ajouté avec succès.")
        elif choix == '4':
            etu_id = input("ID de l'étudiant : ")
            commentaire = input("Commentaire : ")
            montant = input("Montant du bonus : ")
            assign_bonus(etu_id, commentaire, montant)
        elif choix == '5':
            print("Au revoir!")
            break
        else:
            print("Choix invalide. Veuillez sélectionner une option valide.")

if __name__ == "__main__":
    main()
