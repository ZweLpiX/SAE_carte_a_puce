import tkinter as tk
from tkinter import PhotoImage
import subprocess
from PIL import Image, ImageTk

def launch_script(script_name):
    subprocess.run(["python3", f"/home/user/Bureau/Berlicum/{script_name}"])

root = tk.Tk()
root.title("Launcher")

# Chargement et redimensionnement de l'image de café
cafe_image = Image.open("/home/user/Bureau/Berlicum/Img_Berlicum.png")
cafe_image = cafe_image.resize((500, 500))  # Ajustez les dimensions selon vos besoins
cafe_photo = ImageTk.PhotoImage(cafe_image)

# Affichage de l'image
image_label = tk.Label(root, image=cafe_photo)
image_label.pack(pady=10)

# Texte stylisé pour "Menu Principal"
menu_label = tk.Label(root, text="Menu Principal", font=("Cursive", 24, "bold"), fg="brown")
menu_label.pack(pady=10)

# Configuration des couleurs des boutons
button_color = "#4a7abc"  # Bleu
button_text_color = "white"
button_font = ("Helvetica", 12)

# Bouton pour Berlicum
button_berlicum = tk.Button(root, text="Lancer Berlicum", command=lambda: launch_script("GUI_Berlicum.py"), bg=button_color, fg=button_text_color, font=button_font)
button_berlicum.pack(fill=tk.X, pady=5)

root.mainloop()
