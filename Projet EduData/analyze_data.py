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

def import_tle():
    spe_tle = importation_data("data_spe_tle.csv")
    spe_tle_optim = []
    #for i in range(len(spe_tle)):

    return spe_tle

def find(UAI, table):
    result = []
    for i in range (len(table)):
        if UAI  == table[i]['UAI']:
            result.append(table[i])
    return result


table = table_geoloc()
print(find("0860037Y", table))

