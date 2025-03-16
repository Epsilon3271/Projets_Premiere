import os
from PIL import Image

def lister_fichiers(repertoire):
    """Retourne la liste triée des fichiers d'un dossier."""
    return sorted([f for f in os.listdir(repertoire) if f.endswith('.png')])

def extraire_points_lumineux(image):
    """Renvoie les coordonnées des pixels lumineux d'une image."""
    img = Image.open(image).convert("L")
    largeur, hauteur = img.size
    pixels_lumineux = set()

    for y in range(hauteur):
        for x in range(largeur):
            pixel = img.getpixel((x, y))
            if pixel > 200:
                pixels_lumineux.add((x, y))

    return pixels_lumineux


dossier = "telescope02 (1)"
fichiers = lister_fichiers(dossier)

if not fichiers:
    print("Aucune image trouvée dans le dossier.")
    exit()


apparitions = {}

for img in fichiers:
    etoiles = extraire_points_lumineux(os.path.join(dossier, img))
    for etoile in etoiles:
        apparitions[etoile] = apparitions.get(etoile, 0) + 1

etoiles_uniques = {pos for pos, count in apparitions.items() if count == 1}


img_test = Image.open(os.path.join(dossier, fichiers[0]))
resultat = Image.new("RGB", img_test.size, (0, 0, 0))  # Image noire

for x, y in etoiles_uniques:
    resultat.putpixel((x, y), (255, 255, 255))

resultat.show()

