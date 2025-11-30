# Fonction pour le jeu du pendu     
# Auteur : Louise Pericat
# Date : 2025-10-02
#Entrée : saisi d'une lettre susceptible d'être dans le mot 
#Sortie: 

import random


def pendu(mots, tentatives=10):
    mot_choisi = random.choice(mots)  # choisit un mot
    mot_cache = "_" * len(mot_choisi) # mot à deviner sous forme de underscore
    lettres_trouvees = set() #stocke les lettres déjà trouvées
    print("Mot à deviner :", " ".join(mot_cache)) # affiche le mot caché
    while tentatives > 0 and "_" in mot_cache: # tant qu'il reste des tentatives
        print(f"\nTentatives restantes : {tentatives}") # affiche le nombre d'erreur restante
        print("Mot :", " ".join(mot_cache))
        lettre = input("Propose une lettre : ").lower() # si saisie de plus d'une lettre, recommencer
        if len(lettre) != 1 or not lettre.isalpha():
            print("Une lettre seulement.")
            continue
        if lettre in lettres_trouvees:
            print("Lettre déjà proposée.") # si lettre déjà utilisée, recommencer
            continue
        lettres_trouvees.add(lettre) # la nouvelle lettre utilisée est stockée pour ne pas la réutilisée
        if lettre in mot_choisi.lower():
            mot_cache = "".join(
                mot_choisi[i] if mot_choisi[i].lower() in lettres_trouvees else "_"
                for i in range(len(mot_choisi))
            ) # si lettre trouver dans le mot, affiche la lettre a sa place 
            print("Bravo ! Mot actuel : ", " ".join(mot_cache))
        else:
            print("Raté!")
            tentatives -= 1 # enlève un tentative 
    if "_" not in mot_cache:
        print("\nFélicitations ! Le mot est bien :", mot_choisi)
    else:
        print("\nPerdu. Le mot était :", mot_choisi)

def demander_rejouer():
    while True:
        reponse = input("Rejouer ? (o/n) : ").strip().lower()
        if reponse in ["o", "oui"]:
            return True
        elif reponse in ["n", "non"]:
            return False
        else:
            print("Répondre par 'o' ou 'n'.")

def boucle_pendu(mots):
    while True:
        pendu(mots)
        if not demander_rejouer():
            print("Merci d'avoir joué !")
            break


import tkinter as tk
from tkinter import Frame, Label, Button, Toplevel, Message, Entry
import random

class JeuMotus:

    def __init__(self):
        # fenêtre principale
        self.root = tk.Tk()
        self.root.title("Motus")
        self.root.geometry("1100x700")
        self.root.config(bg="#1b2631") 

        # mots du jeu
        self.liste_mots = ["PYTHON", "AVENIR", "POMMES", "LIMACE", "BOUTON", "CHAISE"]

        # création barre de menu 
        self.creer_menu_superieur()

        # titre
        self.labelTitre = Label(
            self.root,
            text="MOTUS",
            fg='white',
            bg="#1b2631",
            font=('fixedsys', 50)
        )
        self.labelTitre.pack(pady=20)

        # zone jeu
        self.cadre_jeu = Frame(self.root, bg="#1b2631")
        self.cadre_jeu.pack()

        # pour stocker grille / widgets
        self.grille_labels = []
        self.champ_saisie = None
        self.bouton_valider = None

        self.afficher_ecran_accueil()

        self.root.mainloop()

    # barre de menu
    def creer_menu_superieur(self):
        self.menu_frame = Frame(self.root, bg="#1b2631", height=60)
        self.menu_frame.pack(fill='x', side='top')

        btn_jouer = Button(self.menu_frame, text="Nouvelle Partie", font=('fixedsys', 18),
                           bg="lightblue", command=self.lancer_partie)
        btn_jouer.pack(side='left', padx=10, pady=10)

        btn_indice = Button(self.menu_frame, text="Indice", font=('fixedsys', 18),
                            bg="lightblue", command=self.reveler_indice)
        btn_indice.pack(side='left', padx=10, pady=10)

        btn_regles = Button(self.menu_frame, text="Règles du jeu", font=('fixedsys', 18),
                            bg="lightblue", command=self.afficher_regles)
        btn_regles.pack(side='left', padx=10, pady=10)

        btn_quitter = Button(self.menu_frame, text="Quitter", font=('fixedsys', 18),
                             bg="lightblue", command=self.root.destroy)
        btn_quitter.pack(side='right', padx=10, pady=10)

    # ecran d'accueil
    def afficher_ecran_accueil(self):
        self.vider_cadre()
        Label(
            self.cadre_jeu,
            text="Clique sur 'Nouvelle partie' pour commencer.",
            font=('fixedsys', 20),
            fg="white", bg="#1b2631"
        ).pack(pady=40)

    # lance une partie
    def lancer_partie(self):
        self.vider_cadre()

        self.mot_secret = random.choice(self.liste_mots)
        self.longueur_mot = len(self.mot_secret)
        self.tentative = 0
        self.tentatives_max = 6
        self.indice_revele = False  # on n'est pas obligé de révéler tout de suite

        cadre_grille = Frame(self.cadre_jeu, bg="#1b2631")
        cadre_grille.pack(pady=20)

        self.grille_labels = []
        for ligne in range(self.tentatives_max):
            ligne_labels = []
            for col in range(self.longueur_mot):
                lbl = Label(
                    cadre_grille,
                    text="",
                    width=4, height=2,
                    font=("fixedsys", 22),
                    relief="ridge", borderwidth=2,
                    bg="#fdfefe", fg="black"
                )
                lbl.grid(row=ligne, column=col, padx=5, pady=5)
                ligne_labels.append(lbl)
            self.grille_labels.append(ligne_labels)

        self.champ_saisie = Entry(self.cadre_jeu, font=("fixedsys", 24), justify="center")
        self.champ_saisie.pack(pady=15)

        self.bouton_valider = Button(
            self.cadre_jeu, text="Valider",
            font=("fixedsys", 20),
            bg="#5dade2", fg="white",
            width=12, command=self.verifier_mot
        )
        self.bouton_valider.pack()

    
    # reveler une lettre (bouton indice)
    def reveler_indice(self):
        if not self.grille_labels:
            return  # aucune partie encore lancée

        if not self.indice_revele:
            self.grille_labels[0][0].config(
                text=self.mot_secret[0],
                bg="#2ecc71",
                fg="white"
            )
            self.indice_revele = True

    # verification du mot saisit
    def verifier_mot(self):
        mot = self.champ_saisie.get().upper()

        if len(mot) != self.longueur_mot:
            tk.messagebox.showwarning("Erreur",
                                    f"Le mot doit contenir {self.longueur_mot} lettres.")
            return

        # remplit la ligne
        for i in range(self.longueur_mot):
            lbl = self.grille_labels[self.tentative][i]
            lbl.config(text=mot[i])

            if mot[i] == self.mot_secret[i]:
                lbl.config(bg="#2ecc71", fg="white")  # vert = bien placé
            elif mot[i] in self.mot_secret:
                lbl.config(bg="#f4d03f")  # jaune
            else:
                lbl.config(bg="#424949", fg="white")  # gris foncé

        if mot == self.mot_secret:
            tk.messagebox.showinfo("Bravo !", f"Tu as trouvé : {self.mot_secret}")
            self.lancer_partie()
            return

        self.tentative += 1

        if self.tentative >= self.tentatives_max:
            tk.messagebox.showinfo("Perdu", f"Le mot était : {self.mot_secret}")
            self.lancer_partie()
            return

        self.champ_saisie.delete(0, tk.END)

    # prendre connaissance des règles
    def afficher_regles(self):
        aide = Toplevel(self.root)
        aide.title("Règles du jeu")
        aide.geometry("600x400")
        aide.config(bg='#1b2631')

        texte = (
            "RÈGLES DU JEU MOTUS\n\n"
            "Devine un mot en 6 tentatives.\n\n"
            "COULEURS :\n"
            "Vert : bonne lettre bien placée\n"
            "Jaune : lettre présente mais mal placée\n"
            "Gris foncé : lettre absente\n\n"
            "Tu peux révéler la première lettre avec le bouton INDICE."
        )

        Message(aide, text=texte, width=560, bg='#1b2631',
                fg='white', font=('fixedsys', 16)).pack(padx=20, pady=20)

        Button(aide, text="Fermer", bg='lightblue',
               command=aide.destroy).pack(pady=10)

    # vider la zone de jeu
    def vider_cadre(self):
        for widget in self.cadre_jeu.winfo_children():
            widget.destroy()



# LANCEMENT
if __name__ == "__main__":
    JeuMotus()



