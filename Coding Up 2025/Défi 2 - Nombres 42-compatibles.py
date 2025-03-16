count =0

def verif_0 (nb):
    if "0" in str(nb):
        return False
    else :
        return True

def produit(nb):
    produit = 1
    for chiffre in str(nb):
        produit *= int(chiffre)
    return produit

def somme(nb):
    somme = 0
    for chiffre in str(nb):
        somme += int(chiffre)
    return somme

for nb in range (178899 ,999762+1):
#for nb in range(0,1000+1):
    if verif_0(nb) == False:
         continue
    else :
        if somme(nb) % 42 == 0 and produit(nb) % 42 == 0:
            count +=1
            print("nb", nb, "count", count)
            #print(nb)
            #print("somme", somme(nb))
            #print("produit", produit(nb))
        else:
            continue
print("********")
print(count)



