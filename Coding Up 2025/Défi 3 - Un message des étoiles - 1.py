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


images_points = [extraire_points_lumineux(os.path.join(dossier, img)) for img in fichiers]


points_communs = set.intersection(*images_points)
etoiles_inconnues = set.union(*images_points) - points_communs


img_test = Image.open(os.path.join(dossier, fichiers[0]))
resultat = Image.new("RGB", img_test.size, (0, 0, 0))

for x, y in etoiles_inconnues:
    resultat.putpixel((x, y), (255, 255, 255))


resultat.show()

