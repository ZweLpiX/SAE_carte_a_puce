import tkinter as tk
import subprocess

# Cette fonction exécute une commande dans un processus séparé et met à jour l'étiquette avec le résultat
def run_command(command, label):
    try:
        # Exécute la commande dans le répertoire spécifié
        subprocess.run(command, cwd="/home/user/Bureau/SAE_Carotte/Rubrovitamin", check=True)
        # Met à jour l'étiquette avec un message de succès
        label.config(text=f"Commande '{' '.join(command)}' exécutée avec succès.")
    except subprocess.CalledProcessError:
        # Met à jour l'étiquette avec un message d'erreur en cas d'échec
        label.config(text=f"Erreur lors de l'exécution de '{' '.join(command)}'.")

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Rubrovitamin Control Panel")

# Création et configuration du cadre supérieur
top_frame = tk.Frame(root, padx=10, pady=10)
top_frame.pack(fill=tk.X)

# Création et configuration du cadre inférieur
bottom_frame = tk.Frame(root, padx=10, pady=5)
bottom_frame.pack(fill=tk.X)

# Label pour afficher les statuts des commandes
status_label = tk.Label(bottom_frame, text="En attente d'une action...", fg="blue")
status_label.pack()

# Bouton pour exécuter 'make'
make_button = tk.Button(top_frame, text="Run Make", command=lambda: run_command(["make"], status_label), bg="lightblue")
make_button.pack(side=tk.LEFT, padx=5)

# Bouton pour exécuter 'make progcarte'
progcarte_button = tk.Button(top_frame, text="Run Make Progcarte", command=lambda: run_command(["make", "progcarte"], status_label), bg="lightgreen")
progcarte_button.pack(side=tk.LEFT, padx=5)

# Bouton pour exécuter 'make clean'
clean_button = tk.Button(top_frame, text="Run Make Clean", command=lambda: run_command(["make", "clean"], status_label), bg="salmon")
clean_button.pack(side=tk.LEFT, padx=5)

# Lancement de la boucle principale de l'interface utilisateur
root.mainloop()

