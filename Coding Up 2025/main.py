from math import isqrt

def diviseurs_propres(nb):
    """Renvoie la somme des diviseurs propres de nb"""
    somme = 1  # 1 est toujours un diviseur propre
    limite = isqrt(nb)
    for i in range(2, limite + 1):
        if nb % i == 0:
            somme += i
            if i != nb // i:  # Éviter d'ajouter le même diviseur deux fois
                somme += nb // i
    return somme

def somme_diviseurs(nb):
    """Renvoie la somme des diviseurs, incluant nb lui-même"""
    return diviseurs_propres(nb) + nb

def est_hautement_abondant(nb):
    """Vérifie si nb est hautement abondant"""
    somme_nb = somme_diviseurs(nb)
    return all(somme_diviseurs(i) < somme_nb for i in range(1, nb))

def est_hautement_abondant_propre(nb):
    """Vérifie si nb est hautement abondant propre"""
    somme_nb = diviseurs_propres(nb)
    return all(diviseurs_propres(i) < somme_nb for i in range(1, nb))

def est_hautement_abondant_sale(nb):
    """Détermine si nb est hautement abondant sale"""
    return est_hautement_abondant(nb) and not est_hautement_abondant_propre(nb)

# Recherche des nombres hautement abondants sales
nombre_abondant_sale = []
i = 1
while len(nombre_abondant_sale)<24:
    if est_hautement_abondant_sale(i) == True:
        nombre_abondant_sale.append(i)
        print(nombre_abondant_sale)
    i+=1


print(nombre_abondant_sale)
