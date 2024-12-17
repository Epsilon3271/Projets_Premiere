from PIL import Image

def txt_to_bin(txt_clair):
    txt_binaire = ""
    for lettres in txt_clair:
        binaire = str(bin(ord(lettres)))
        txt_binaire += binaire[2:].zfill(8)
    bin_to_list(txt_binaire)
    return txt_binaire

def bin_to_list(txt_binaire):
    txt_bin_list = []
    for el in txt_binaire:
        txt_bin_list.append(int(el))
    size_txt_bin(txt_bin_list)
    return txt_bin_list

def size_txt_bin(txt_bin):
    size_txt = len(txt_bin)
    size_txt_binaire = str(bin(size_txt))[2:].zfill(16)
    return size_txt_binaire

def hide_msg(user_input, img_origine_path):

    txt_clair = str(user_input)
    #print(txt_clair)
    #txt_bin = txt_to_bin(txt_clair)
    #print(txt_bin)
    #txt_bin_list = bin_to_list(txt_bin)
    #print(txt_bin_list)

    #size_txt = size_txt_bin(txt_bin_list)
    #print(size_txt)
    #size_txt_liste = bin_to_list(size_txt)
    #print(size_txt_liste)

    txt_bin_tot =[]

    for el in bin_to_list(size_txt_bin(bin_to_list(txt_to_bin(txt_clair)))):
        txt_bin_tot.append(int(el))
    for el in bin_to_list(txt_to_bin(txt_clair)):
        txt_bin_tot.append(int(el))
    print(txt_to_bin(txt_clair))
    print(txt_bin_tot)



    img_init = Image.open(str(img_origine_path))
    L, H = img_init.size

    size_txt_tot = len(bin_to_list(txt_to_bin(txt_clair)))
    print(size_txt_tot)

    if size_txt_tot > L*H:
        return "La taille de l'image ne peut supporter le texte"

    img_encode = Image.new("RGB", (L, H))

    indice = 0

    for y in range(H):
        for x in range(L):
            pixel = img_init.getpixel((x, y))
            if indice >= size_txt_tot:
                img_encode.putpixel((x, y), pixel)
            else:
                if txt_bin_tot[indice] == 0:
                    if pixel[0] % 2 != 0:
                        img_encode.putpixel((x, y), (pixel[0] + 1,pixel[1],pixel[2]))
                    else:
                        img_encode.putpixel((x, y), pixel)

                else:
                    if pixel[0] % 2 != 0:
                        img_encode.putpixel((x, y), pixel)
                    else:
                        img_encode.putpixel((x, y), (pixel[0] + 1,pixel[1],pixel[2]))

                indice += 1

    img_encode.save("Image_encode2.png")


hide_msg("votre texte", "chemin vers l'image")
