import tkinter as tk
import subprocess

def run_command(command, label):
    try:
        subprocess.run(command, cwd="/home/user/Bureau/SAE_Carotte/Rubrovitamin", check=True)
        label.config(text=f"Commande '{' '.join(command)}' exécutée avec succès.")
    except subprocess.CalledProcessError:
        label.config(text=f"Erreur lors de l'exécution de '{' '.join(command)}'.")

root = tk.Tk()
root.title("Rubrovitamin Control Panel")

top_frame = tk.Frame(root, padx=10, pady=10)
top_frame.pack(fill=tk.X)

bottom_frame = tk.Frame(root, padx=10, pady=5)
bottom_frame.pack(fill=tk.X)

status_label = tk.Label(bottom_frame, text="En attente d'une action...", fg="blue")
status_label.pack()

make_button = tk.Button(top_frame, text="Run Make", command=lambda: run_command(["make"], status_label), bg="lightblue")
make_button.pack(side=tk.LEFT, padx=5)

progcarte_button = tk.Button(top_frame, text="Run Make Progcarte", command=lambda: run_command(["make", "progcarte"], status_label), bg="lightgreen")
progcarte_button.pack(side=tk.LEFT, padx=5)

clean_button = tk.Button(top_frame, text="Run Make Clean", command=lambda: run_command(["make", "clean"], status_label), bg="salmon")
clean_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
