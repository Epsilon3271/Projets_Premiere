import random  # Importation du module random pour générer des nombres aléatoires

def stockage(points):
    """
    Enregistre le score d'une partie dans un fichier texte.

    Paramètres :
    - points (float) : Le score à enregistrer.

    Fonctionnement :
    - Ouvre (ou crée) le fichier 'score.txt' en mode ajout.
    - Écrit le score à la fin du fichier.
    - Gère les erreurs si le fichier est introuvable.
    """
    try:
        with open("score.txt", "a") as fichier:  # Ouvre le fichier en mode ajout
            fichier.write("\n")  # Ajoute une nouvelle ligne
            fichier.write(str(points))  # Écrit le score
    except FileNotFoundError:  # Si le fichier n'existe pas
        print("Erreur : le fichier 'score.txt' est introuvable. Contactez le développeur.")

def tableau():
    """
    Affiche un tableau contenant les scores enregistrés.

    Fonctionnement :
    - Ouvre le fichier 'score.txt'.
    - Lit et affiche chaque score avec son numéro de partie.
    - Gère les erreurs si le fichier est introuvable.
    """
    try:
        # Récupère les scores depuis le fichier
        liste_scores = list(open('score.txt'))
        print("---------------------------")
        # Affiche chaque score avec son numéro
        for i, score in enumerate(liste_scores):
            index = str(i + 1)
            print(f"| Score partie {index.rjust(3)} | {score.strip().rjust(4)} |")
        print("---------------------------")
    except FileNotFoundError:  # Si le fichier n'existe pas
        print("Erreur : le fichier 'score.txt' est introuvable.")

def Quiz(niveau):
    """
    Lance le quiz en fonction du niveau choisi.

    Paramètres :
    - niveau (int) : Nombre de questions dans le quiz.

    Fonctionnement :
    - Charge aléatoirement des questions et réponses depuis des fichiers.
    - Permet à l'utilisateur de répondre avec un maximum de 5 essais par question.
    - Enregistre le score final et retourne au menu principal.
    """
    print("\nPendant le quiz, écrivez 7700 à tout moment pour arrêter la partie.")
    points = 0  # Initialise le score

    for i in range(niveau):  # Itère sur le nombre de questions
        try:
            # Ouvre le fichier des questions et sélectionne une question aléatoire
            with open('questions.txt', 'r', encoding='utf-8') as fichier:
                lignes = fichier.readlines()
                rang_question = random.randint(1, len(lignes) - 1)  # Numéro de la question
                question = lignes[rang_question].strip()  # Récupère la question
        except FileNotFoundError:
            print("Erreur : le fichier 'questions.txt' est introuvable.")
            return

        try:
            # Ouvre le fichier des réponses et récupère la réponse associée
            with open("reponses.txt", "r", encoding='utf-8') as fichier:
                lignes = fichier.readlines()
                reponse = lignes[rang_question].strip()
        except FileNotFoundError:
            print("Erreur : le fichier 'reponses.txt' est introuvable.")
            return

        essais = 1  # Initialise le compteur d'essais

        while True:
            try:
                # Demande une réponse à l'utilisateur
                rep_user = int(input(question + " "))
            except ValueError:
                print("Veuillez entrer une année valide (nombre).")
                continue

            if rep_user == 7700:  # Code d'arrêt pour quitter la partie
                print("Partie interrompue. Score enregistré.")
                stockage(points)
                Menu()
                return

            if rep_user == int(reponse):  # Vérifie si la réponse est correcte
                print(f"Bonne réponse ! Score gagné : {1 / essais:.2f}")
                points += 1 / essais  # Ajoute le score en fonction des essais
                break
            else:
                if essais == 5:  # Si les essais sont épuisés
                    print("Dommage, vous avez utilisé vos 5 essais.")
                    break
                # Informe si la réponse est supérieure ou inférieure
                if rep_user > int(reponse):
                    print("La bonne réponse est inférieure.")
                else:
                    print("La bonne réponse est supérieure.")
                essais += 1  # Incrémente le nombre d'essais

    print(f"Fin du quiz ! Votre score : {points:.2f}")
    stockage(points)  # Enregistre le score
    Menu()  # Retourne au menu principal

def Jeu():
    """
    Permet de choisir le niveau de difficulté et lance le quiz.

    Fonctionnement :
    - Propose trois niveaux : Facile (5 questions), Moyen (10 questions), Difficile (20 questions).
    - Appelle la fonction Quiz avec le nombre de questions correspondant.
    """
    while True:
        try:
            # Demande le choix du niveau
            chx = input("Choisissez un niveau : Facile, Moyen, Difficile : ")
            assert chx in ["Facile", "Moyen", "Difficile"]
            break
        except AssertionError:
            print("Veuillez entrer un niveau valide (Facile, Moyen, Difficile).")

    if chx == "Facile":
        Quiz(5)
    elif chx == "Moyen":
        Quiz(10)
    elif chx == "Difficile":
        Quiz(20)

def AddQ():
    """
    Permet d'ajouter une nouvelle question et sa réponse.

    Fonctionnement :
    - Demande une question à l'utilisateur.
    - Demande la réponse associée.
    - Ajoute les deux dans les fichiers 'questions.txt' et 'reponses.txt'.
    """
    try:
        # Ajoute une question au fichier
        with open('questions.txt', 'a', encoding='utf-8') as fichier:
            question = input("Entrez votre nouvelle question : ")
            fichier.write("\n" + question)
    except FileNotFoundError:
        print("Erreur : le fichier 'questions.txt' est introuvable.")

    try:
        # Ajoute une réponse au fichier
        with open('reponses.txt', 'a', encoding='utf-8') as fichier:
            reponse = input("Entrez la réponse à cette question : ")
            fichier.write("\n" + reponse)
    except FileNotFoundError:
        print("Erreur : le fichier 'reponses.txt' est introuvable.")

def Menu():
    """
    Affiche le menu principal du programme.

    Fonctionnement :
    - Propose trois options : Quiz, Tableau des scores, Ajouter des questions.
    - Redirige vers la fonction correspondante.
    """
    print("Bienvenue dans le Quiz d'histoire !")
    while True:
        try:
            # Affiche les options du menu
            chx = input("Options : Quiz, Scores, AddQ : ")
            assert chx in ["Quiz", "Scores", "AddQ"]
            break
        except AssertionError:
            print("Veuillez entrer une option valide (Quiz, Scores, AddQ).")

    if chx == "Quiz":
        Jeu()
    elif chx == "Scores":
        tableau()
        Menu()  # Retourne au menu après affichage
    elif chx == "AddQ":
        AddQ()
        Menu()  # Retourne au menu après ajout

# Lancement du programme
Menu()
