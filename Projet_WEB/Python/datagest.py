import sqlite3

# Ouvrir la connexion à la base de données
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

def add_qte(jour, qte):
    """Ajoute ou met à jour la quantité d'un jour dans la table ventes."""
    cursor.execute("""
        INSERT INTO ventes (Jours, Qte) VALUES (?, ?)
        ON CONFLICT(Jours) DO UPDATE SET Qte = Qte + excluded.Qte
    """, (jour, qte))
    conn.commit()

def cut():
    """Supprime toutes les données de la table ventes."""
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ventes")  # Correction : plus de sqlite_sequence
        conn.commit()

def print_data():
    """Affiche les données de la table ventes."""
    cursor.execute("SELECT * FROM ventes")
    resultats = cursor.fetchall()

    print("Jours -- Qte")
    for jour, qte in resultats:
        print(f"{jour:<10} {qte}")

# Création de la table si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS ventes (
    Jours TEXT PRIMARY KEY,
    Qte INTEGER
)
""")
conn.commit()

# Menu interactif
chx = int(input(f"Quelle action voulez-vous faire sur la base de données ? \n 1: Supprimer l'ensemble des données \n 2: Ajouter des données \n 3: Afficher les données \n 4: Fermer le programme\n"))

if chx == 1:
    cut()
elif chx == 2:
    jour = input("Entrez le jour : ")
    qte = int(input("Entrez la quantité de portions : "))  # Conversion en int
    add_qte(jour, qte)
elif chx == 3:
    print_data()
else:
    print("Fermeture du programme.")

conn.close()  # Ferme la connexion seulement à la fin
