# Import des librairies et fichier nécessaires

import tkinter as tk
from tkinter import ttk
from scripts import multi, solo, demo

"""
Fenetre principale
Affichage de l'interface principal pour choisir son mode de jeu et me nombre de boules désiré:
  - encadré de saisie -> saisie du pseudo voulu pour le mode multijoueur
  -> choix du mode de jeu désiré
  - bouton "MODE SOLO" -> Ouvre la fenêtre de jeu du mode solo
  - bouton "MODE DE DEMONSTRATION" -> Ouvre la fenêtre de jeu du mode de démonstration
  - bouton "MODE MULTIJOUEUR" -> Ouvre la fenêtre de jeu du mode multijoueur
  - bouton "QUITTER LE JEU" -> Ferme la fenêtre du jeu
"""

#Initialisation de la fenêtre (image de fond, police, taille, ..)
root = tk.Tk()
root.title("Bubble")
root.geometry("600x400")
bg_image = tk.PhotoImage(file="assets/main-bg.gif")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0)


# création du titre de la fenêtre
libTitre = tk.Label(root,
                    text="Bubble",
                    font=("Courier ", 20),
                    foreground='white',
                    background='blue')
libTitre.place(x=0, y=0, width=600)

# Zone de saisie du nombre de boules souhaitées pour la partie
libJeu = tk.Label(root, text="Pseudo souhaité pour le mode multijoueur :", font=("Courier", 10))
libJeu.place(x=125, y=50)
libJeu.config(background="#FFFFFF")
saisieJeu = tk.Text(root, height=1)
saisieJeu.place(x=240, y=75, width=120)

"""
Définition des fonctions d'exécution :
- Fonction launch_demo_mode -> permet d'executer le programme associé au mode de démonstration
- Fonction launch_solo_mode -> permet d'executer le programme associé au mode solo
- Fonction launch_multi_mode -> permet d'executer le programme associé au mode multijoueur 
"""

# Fonction qui execute le programme associé au mode démo lorsque le bouton est cliqué
def launch_demo_mode():
    root.destroy()
    demo.main(100, 1200, 800)

# Fonction qui execute le programme associé au mode solo lorsque le bouton est cliqué
def launch_solo_mode():
    root.destroy()
    solo.main(30)

# Fonction qui execute le programme associé au mode multijoueur lorsque le bouton est cliqué
def launch_multi_mode():
    global saisieJeu
    pseudo = saisieJeu.get(1.0, tk.END)
    root.destroy()
    multi.main(pseudo.replace("\n", ""))


# Bouton MODE DE DEMONSTRATION
bt_execution = tk.Button(root, text="MODE DE DEMONSTRATION", font=("Courier", 10), command=launch_demo_mode)
bt_execution.place(x=20, y=200, width=175, height=100) # Place et taille du bouton

# Bouton MODE SOLO
bt_execution = tk.Button(root, text="MODE SOLO", font=("Courier", 10), command=launch_solo_mode)
bt_execution.place(x=215, y=200, width=175, height=100) # Place et taille du bouton

# Bouton MODE MULTIJOUEUR
bt_execution = tk.Button(root, text="MODE MULTIJOUEUR", font=("Courier", 10), command=launch_multi_mode)
bt_execution.place(x=410, y=200, width=175, height=100) # Place et taille du bouton

# Bouton QUITTER LE JEU
bt_execution = tk.Button(root, text="QUITTER LE JEU", font=("Courier", 10), bg='#ea4258', command=root.destroy)
bt_execution.place(x=215, y=315, width=175, height=75) # Place et taille du bouton


#  Mise à jour en permanence des variables du formulaire
root.resizable(width=False, height=False) # commande permettant de verouiller la fenetre
root.mainloop()