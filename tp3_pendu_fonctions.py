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





