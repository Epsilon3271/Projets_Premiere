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
    for lettres in txt_clair:  # Convertit chaque caractère en sa valeur binaire sur 8 bits.
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
    return [int(el) for el in txt_binaire]  # Conversion en liste du texte en binaire grâce à un tableau construit par compréhension.

def size_txt_bin(txt_bin):
    """
    Calcule la taille en binaire (sur 16 bits) d'une chaîne binaire.

    Parametres:
        txt_bin (str): Une chaîne binaire.

    Returns:
        str: Taille de la chaîne binaire en représentation binaire sur 16 bits.
    """
    size_txt = len(txt_bin)  # Mesure la taille du texte.
    return str(bin(size_txt))[2:].zfill(16)  # Convertit la taille mesurée en binaire sur 16 bits.

def hide_msg(user_input, img_origine_path):
    """
    Cache un message texte dans une image via la méthode LSB (Least Significant Bit).

    Parametres:
        user_input (str): Le texte à cacher.
        img_origine_path (str): Le chemin vers l'image d'origine.

    Returns:
        str: Un message d'erreur si la taille de l'image est insuffisante, sinon rien.
    """
    try:
        txt_clair = str(user_input)
        txt_bin = txt_to_bin(txt_clair)
        txt_size_bin = size_txt_bin(txt_bin)

        
        txt_bin_tot = bin_to_list(txt_size_bin) + bin_to_list(txt_bin)  # Crée la liste totale binaire (16 bits pour la taille + texte).

        img_init = Image.open(img_origine_path)  # Charge l'image d'origine.
        L, H = img_init.size  # Récupère les dimensions de l'image.

        if len(txt_bin_tot) > L * H:  # Vérifie si l'image est assez grande pour contenir le texte.
            return "La taille de l'image ne peut supporter le texte."

        img_encode = Image.new("RGB", (L, H))  # Nouvelle image pour stocker les données.

        index = 0  # Indice pour parcourir les bits du message.
        for y in range(H):
            for x in range(L):
                pixel = img_init.getpixel((x, y))  # Récupère le pixel d'origine.

                if index < 16:  # Encodage des 16 premiers bits pour la taille
                    bit = int(txt_size_bin[index])
                    red = pixel[0]

                    if bit == 1:
                        if red % 2 == 0:
                            red += 1
                    else:
                        if red % 2 == 1:
                            red -= 1

                    img_encode.putpixel((x, y), (red, pixel[1], pixel[2]))
                    index += 1

                elif index < len(txt_bin_tot):
                    bit = txt_bin_tot[index]
                    red = pixel[0]

                    if bit == 1:
                        if red % 2 == 0:
                            red += 1
                    else:
                        if red % 2 == 1:
                            red -= 1

                    img_encode.putpixel((x, y), (red, pixel[1], pixel[2]))
                    index += 1

                else:
                    img_encode.putpixel((x, y), pixel)  # Copie le pixel d'origine si aucun bit n'est à encoder.

        img_encode.save("Image_encode.png")  # Sauvegarde l'image encodée.
        print("L'image a été encodée et sauvegardée sous le nom 'Image_encode.png'.")

    except FileNotFoundError:
        return "Erreur : Le fichier image spécifié est introuvable."
    except Exception as e:
        return f"Erreur inattendue : {e}"


if __name__ == "__main__":
    msg = input("Entrez le message à cacher : ")
    path = input("Entrez le chemin d'accès à l'image originale : ")
    result = hide_msg(msg, path)
    if result:
        print(result)
