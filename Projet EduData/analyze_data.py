# Table effectif total pr lycée [UAI, ANNEE, EFFECTIF TOTAL]
import csv
from csv import DictReader
def importation_data(fichier):
    with open(fichier, encoding = "utf-8-sig") as f:
        u = []
        for dict in DictReader(f, delimiter=';'):
            u.append(dict)
    return u
def table_geoloc():
    geoloc = []
    table_init = importation_data('geolocalisation.csv')
    for i in range(len(table_init)):
        denomination = table_init[i]["denomination_principale"]
        if (("LYCEE" in denomination) or ("GENERAL" in denomination) or ("POLYVALENT" in denomination)) and ("PROFESSIONNEL" not in denomination):
            geoloc.append({"UAI": table_init[i]["UAI"],"LAT": table_init[i]["latitude"],"LONG": table_init[i]["longitude"]})
    return geoloc
def table_effectifs():
    effectifs = []
    etablissement = importation_data("effectif_total.csv")
    for i in range(len(etablissement)):
        effectifs.append({"UAI" : etablissement[i]["UAI"], "ANNEE": etablissement[i]["Rentrée scolaire"],"EFTOT": etablissement[i]["Nombre d'élèves"]})
    return effectifs
def table_fiche_etab():
    fiche_etab = []
    uai_vus = set()

    etablissement = importation_data("data_spe_1er.csv")
    geoc = table_geoloc()
    effectifs = table_effectifs()

    # Dictionnaire pour accéder rapidement aux coordonnées
    geoc_dict = {entry["UAI"]: {"LAT": entry["LAT"], "LONG": entry["LONG"]} for entry in geoc}

    # Dictionnaire pour accéder rapidement à l’effectif total
    effectif_dict = {entry["UAI"]: entry["EFTOT"] for entry in effectifs}

    for e in etablissement:
        uai = e["UAI"]
        if uai not in uai_vus and uai in geoc_dict:
            uai_vus.add(uai)
            fiche_etab.append({"UAI": uai,"DENO": e["DENOMINATION PRINCIPALE"],"NOM": e["PATRONYME"],"TYPE": e["SECTEUR"],"ACA": e["ACADEMIE"],"DEPA": e["DEPARTEMENT"],"VILLE": e["COMMUNE"],"LAT": geoc_dict[uai]["LAT"],"LONG": geoc_dict[uai]["LONG"],"EFTOT": effectif_dict.get(uai)})

    return fiche_etab

def find(UAI, table):
    result = []
    for i in range (len(table)):
        if UAI  == table[i]['UAI']:
            result.append(table[i])
    return result


table = table_fiche_etab()
print(find("0860037Y", table))
#print(table_fiche_etab())
