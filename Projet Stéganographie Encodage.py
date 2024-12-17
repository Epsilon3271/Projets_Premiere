from PIL import Image

def txt_to_bin(txt_clair):
    """
    Convertit un texte clair en une chaîne binaire.

    Parametres:
        txt_clair (str): Le texte à convertir.

    Returns:
        str: Une chaîne représentant le texte en binaire.
    """
    txt_binaire = ""
    for lettres in txt_clair:
        # Convertit chaque caractère en sa valeur binaire et le remplit pour faire 8 bits.
        binaire = str(bin(ord(lettres)))
        txt_binaire += binaire[2:].zfill(8)
    return txt_binaire

def bin_to_list(txt_binaire):
    """
    Convertit une chaîne binaire en une liste d'entiers.

    Parametres:
        txt_binaire (str): Une chaîne binaire.

    Returns:
        list: Liste d'entiers (0 ou 1) correspondant à chaque bit.
    """
    txt_bin_list = []
    for el in txt_binaire:
        # Ajoute chaque bit sous forme d'entier à la liste.
        txt_bin_list.append(int(el))
    return txt_bin_list

def size_txt_bin(txt_bin):
    """
    Calcule la taille en binaire (sur 16 bits) d'une chaîne binaire.

    Parametres:
        txt_bin (str): Une chaîne binaire.

    Returns:
        str: Taille de la chaîne binaire en représentation binaire sur 16 bits.
    """
    size_txt = len(txt_bin)
    # Convertit la taille en binaire sur 16 bits.
    size_txt_binaire = str(bin(size_txt))[2:].zfill(16)
    return size_txt_binaire

def hide_msg(user_input, img_origine_path):
    """
    Cache un message texte dans une image via la méthode LSB (Least Significant Bit).

    Parametres:
        user_input (str): Le texte à cacher.
        img_origine_path (str): Le chemin vers l'image d'origine.

    Returns:
        str: Un message d'erreur si la taille de l'image est insuffisante, sinon rien.
    """
    txt_clair = str(user_input)
    txt_bin_tot = []

    for el in bin_to_list(size_txt_bin(bin_to_list(txt_to_bin(txt_clair)))):    # Ajoute d'abord la taille du texte en binaire (16 bits), puis le texte en binaire.
        txt_bin_tot.append(int(el))
    for el in bin_to_list(txt_to_bin(txt_clair)):
        txt_bin_tot.append(int(el))

    img_init = Image.open(str(img_origine_path))  # Charge l'image d'origine.
    L, H = img_init.size  # Dimensions de l'image.

    size_txt_tot = len(bin_to_list(txt_to_bin(txt_clair)))  # Taille totale du texte en bits.

    if size_txt_tot > L * H:    # Vérifie si l'image est assez grande pour contenir le texte.
        return "La taille de l'image ne peut supporter le texte"

    img_encode = Image.new("RGB", (L, H))  # Nouvelle image pour stocker les données.

    index = 0  # Indice pour parcourir les bits du message.

    for y in range(H):  # Parcourt chaque pixel de l'image.
        for x in range(L):
            pixel = img_init.getpixel((x, y))  # Récupère le pixel courant.
            if index >= size_txt_tot:   # Si tous les bits sont encodés, copie le reste des pixels tels quels.
                img_encode.putpixel((x, y), pixel)
            else:
                if txt_bin_tot[index] == 0:
                    if pixel[0] % 2 != 0:   # Si le bit est 1, on s'assure que le LSB du canal rouge est impair.
                        img_encode.putpixel((x, y), (pixel[0] + 1, pixel[1], pixel[2]))
                    else:
                        img_encode.putpixel((x, y), pixel)
                else:
                    if pixel[0] % 2 != 0:   # Si le bit est 1, on s'assure que le LSB du canal rouge est impair.
                        img_encode.putpixel((x, y), pixel)
                    else:
                        img_encode.putpixel((x, y), (pixel[0] + 1, pixel[1], pixel[2]))

                index += 1  # Passe au bit suivant.

    
    img_encode.save("Image_encode2.png")    # Sauvegarde l'image encodée.


hide_msg("votre texte", "Image.png")
