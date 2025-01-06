from PIL import Image

def decode(nom_image):
    """
    Retourne le message dans l'image

    Inputs
    ------
    image:nom de l'image
        Nom de l'image contenant le message

    Returns
    -------
    str
        Message contenu dans l'image
    """

    # Ouvrir l'image
    try:
        image = Image.open(nom_image)
    except FileNotFoundError:
        return "Erreur : Le fichier image spécifié est introuvable."

    # Regarder la taille de l'image
    longueur = 17 # Nombre de bits définissant la taille du message
    binaire = ""

    for y in range(longueur):
        if longueur == 0:
            break
        for x in range(longueur):
            longueur -= 1
            if longueur == 0:
                break
            binaire += str(int(image.getpixel((x,y))[0] % 2 != 0))

    taille = int(binaire, 2) + 16

    # Regarder la suite et extraire le binaire
    binaire = ""
    index = (x, y) # Index où reprendre
    for y in range(0, image.height):
        if taille <= 0:
            break
        for x in range(0, image.width):
            if taille <= 0:
                break

            taille -= 1

            binaire += str(int(image.getpixel((x,y))[0] % 2 != 0))

    # Transformer le binaire en texte
    res = binaire_to_text(binaire[16:])

    return res

def binaire_to_text(binaire):
    """
    Retournes le texte correspondant au code binaire

    Inputs
    ------
    binaire:str
        Texte en binaire

    Return
    ------
    str
        Texte normal
    """

    texte = ""
    last = 0

    for index in range(8, len(binaire)+1, 8):
        car = binaire[last:index]


        # Binaire -> Décimal
        dec = 0

        for i in range(len(car)):
            dec += int(car[i]) * 2**(len(car)-i-1)

        # Décimal -> ASCII
        texte += chr(dec)

        last = index

    return texte

if __name__ == "__main__":
    print(decode("image_encode.png"))
