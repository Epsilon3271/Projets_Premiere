from PIL import Image

img_init = Image.open("C25_Image_42_encoded.png")  # Charge l'image d'origine.
L, H = img_init.size  # Récupère les dimensions de l'image.
img_decode = Image.new("RGB", (L, H))  # Nouvelle image pour stocker les données.

for y in range(H):
    for x in range(L):
        pixel = img_init.getpixel((x, y))  # Récupère le pixel d'origine.
        somme = 16*pixel[0] + 4*pixel[1] + pixel[2]
        if somme%42 == 0:
            img_decode.putpixel((x,y), (0, 0, 0))
        else:
            img_decode.putpixel((x,y), (pixel[0], pixel[1], pixel[2]))
img_decode.show()

