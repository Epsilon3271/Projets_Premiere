# Table effectif total pr lycée [UAI, ANNEE, EFFECTIF TOTAL]
import csv
from csv import DictReader
import folium

carte = folium.Map(location=[48.8566, 2.3522], zoom_start=13, tiles="CartoDB dark_matter") # Ou "CartoDB positron" pour meme fond de carte mais en blanc
def importation_data(fichier):
    with open(fichier, encoding="utf-8-sig") as f:
        lecteur = DictReader(f, delimiter=';')
        keys = lecteur.fieldnames
        u = []
        for ligne in lecteur:
            u.append(ligne)
    return u
def return_keys(fichier):
    with open(fichier, encoding="utf-8-sig") as f:
        lecteur = DictReader(f, delimiter=';')
        keys = lecteur.fieldnames
    return keys
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
def carte_create(nom,type,ville, academie, departement):
    etab = table_fiche_etab()
    for i in range(len(etab)):
        if ((nom and nom.upper() == etab[i]["NOM"]) or
                (type and type.upper() == etab[i]["TYPE"]) or
                (ville and ville.upper() == etab[i]["VILLE"]) or
                (academie and academie.upper() == etab[i]["ACA"]) or
                (departement and departement.upper() == etab[i]["DEPA"])):

            lat_str = etab[i]["LAT"]
            lon_str = etab[i]["LONG"]

            if lat_str and lon_str:  # Vérifie que les valeurs ne sont pas vides
                try:
                    lat = float(lat_str)
                    lon = float(lon_str)
                    folium.Marker(location=[lat, lon], popup=f"{etab[i]['DENO']} \n {etab[i]['NOM']}",max_width=200,icon=folium.Icon(color="gray", icon="university", prefix="fa")).add_to(carte)
                except ValueError as e:
                    print(f"Erreur de conversion pour les coordonnées ({lat_str}, {lon_str}): {e}")
            else:
                print(f"Coordonnées manquantes pour UAI {etab[i]['UAI']}")
def spe_1er():
    spe1er = []
    data = importation_data("data_spe_1er.csv")
    keys = return_keys("data_spe_1er.csv")

    for i in range(len(data)):
        spe = {
            "UAI": data[i]["UAI"],
            "ANNEE": data[i]["RENTREE SCOLAIRE"],
            "EFTOT": data[i]["EFFECTIF TOTAL"],
            "EFTOTF": data[i]["EFFECTIF TOTAL FILLES"],
            "EFTOTG": data[i]["EFFECTIF TOTAL GARCONS"]
        }

        for y in range(17, len(keys)):
            val = data[i][keys[y]]
            if val != "0" and val != "":
                spe[keys[y]] = val

        spe1er.append(spe)

    return spe1er
def spe_tle():
    spetle = []
    data = importation_data("data_spe_tle.csv")
    keys = return_keys("data_spe_tle.csv")

    for i in range(len(data)):
        spe = {
            "UAI": data[i]["UAI"],
            "ANNEE": data[i]["Rentrée scolaire"],
            "EFTOT": data[i]["Effectif total"],
            "EFTOTF": data[i]["Effectif total filles"],
            "EFTOTG": data[i]["Effectif total garçons"]
        }

        for y in range(17, len(keys)):
            val = data[i][keys[y]]
            if val != "0" and val != "":
                spe[keys[y]] = val

        spetle.append(spe)

    return spetle
def find(UAI, table):
    result = []
    for i in range(len(table)):
        if UAI == table[i]['UAI']:
            result.append(table[i])
    return result
def statistica(table, uai):
    pass




carte_create(None,None,None, "Poitiers", None)
carte.save("carte.html")
#table = table_fiche_etab()
#print(find("0860037Y", table))
#print(table_fiche_etab())

#table = spe_1er()
#print(find("0860037Y", table))
