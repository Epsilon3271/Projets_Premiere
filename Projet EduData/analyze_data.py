# Table effectif total pr lycée [UAI, ANNEE, EFFECTIF TOTAL]
from csv import DictReader
import folium
import plotly.graph_objects as pg
from plotly.subplots import make_subplots
import math
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
def k(dictionnaire):
    return list(dictionnaire.keys())
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
def carte_create(nom,type,ville, academie, departement):
    carte = folium.Map(location=[48.8566, 2.3522], zoom_start=13,tiles="CartoDB dark_matter")  # Ou "CartoDB positron" pour meme fond de carte mais en blanc
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

                    # Génère le fichier HTML pour les graphiques
                    statistica(etab[i]["UAI"])

                    # Contenu HTML du popup avec lien cliquable
                    popup_html = f"""
                    <b>{etab[i]['DENO']}</b><br>
                    {etab[i]['NOM']}<br>
                    <a href="graphiques_effectifs_{etab[i]['UAI']}.html" target="_blank">Voir les données</a>
                    """

                    # Ajout du marqueur avec popup adapté
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_html, max_width=300),
                        icon=folium.Icon(color="gray", icon="university", prefix="fa")
                    ).add_to(carte)

                except ValueError as e:
                    print(f"Erreur de conversion pour les coordonnées ({lat_str}, {lon_str}): {e}")
            else:
                print(f"Coordonnées manquantes pour UAI {etab[i]['UAI']}")
def statistica(uai):
    titres = ["Première", "Terminale"]
    fig = make_subplots(rows=1, cols=2,subplot_titles=titres)

    fiche_etab = table_fiche_etab()
    for i in range(len(fiche_etab)):
        if fiche_etab[i]["UAI"] == uai:
            nom = fiche_etab[i]["NOM"]
            break

    pr = spe_1er()
    tle = spe_tle()
    data_pr = sorted(find(uai, pr), key=lambda x: x["ANNEE"])
    data_tle = sorted(find(uai, tle), key=lambda x: x["ANNEE"])

    # Création des listes de données
    annees_pr = [int(x["ANNEE"]) for x in data_pr]
    eftot_pr = [int(x["EFTOT"]) for x in data_pr]
    eftotf_pr = [int(x["EFTOTF"]) for x in data_pr]
    eftotg_pr = [int(x["EFTOTG"]) for x in data_pr]

    # Ajout des courbes pour la première
    fig.add_trace(pg.Scatter(x=annees_pr, y=eftot_pr, name='Total 1ère', line=dict(color='red')), row=1, col=1)
    fig.add_trace(pg.Scatter(x=annees_pr, y=eftotf_pr, name='Filles 1ère', line=dict(color='hotpink')), row=1,col=1)
    fig.add_trace(pg.Scatter(x=annees_pr, y=eftotg_pr, name='Garçons 1ère', line=dict(color='blue')), row=1, col=1)

    # Création des listes de données
    annees_tle = [int(x["ANNEE"]) for x in data_tle]
    eftot_tle = [int(x["EFTOT"]) for x in data_tle]
    eftotf_tle = [int(x["EFTOTF"]) for x in data_tle]
    eftotg_tle = [int(x["EFTOTG"]) for x in data_tle]

    # Ajout des courbes pour la terminale
    fig.add_trace(pg.Scatter(x=annees_tle, y=eftot_tle, name='Total Tle', line=dict(color='red')), row=1, col=2)
    fig.add_trace(pg.Scatter(x=annees_tle, y=eftotf_tle, name='Filles Tle', line=dict(color='hotpink')), row=1,col=2)
    fig.add_trace(pg.Scatter(x=annees_tle, y=eftotg_tle, name='Garçons Tle', line=dict(color='blue')), row=1, col=2)


    # annees_pr_spe=[]
    # eftotf_pr_spe=[]
    # eftotg_pr_spe = []
    #
    # for i in range(len(data_pr)):
    #     if data_pr[i]["UAI"] == uai:
    #         keys = k(data_pr[i])
    #         for y in range(4,len(keys) - 1):
    #             if str(keys[y])[:4] == str(keys[y + 1])[:4]:
    #                 annees_pr_spe.append(int(data_pr[i]["ANNEE"]))
    #                 eftotf_pr_spe.append(int(data_pr[i][keys[y]]))
    #                 eftotg_pr_spe.append(int(data_pr[i][keys[y + 1]]))
    #                 break
    # titres.append(str(keys[y][6:-10]))
    #
    # fig.add_trace(pg.Scatter(x=annees_pr_spe, y=eftotf_pr, name='Total Tle', line=dict(color='hotpink')), row=1, col=3)
    # fig.add_trace(pg.Scatter(x=annees_pr_spe, y=eftotg_pr, name='Filles Tle', line=dict(color='blue')), row=1,col=3)



    fig.update_layout(
        title_text=f"Évolution des effectifs filles/garçons en première et terminale dans le lycée {nom}",
        xaxis_title="Année",
        yaxis_title="Effectif",
        showlegend=True
    )

    fig.write_html(f"graphiques_effectifs_{uai}.html", auto_open=False)

#carte_create(None,None,"Poitiers", None, None)
#carte.save("carte.html")
#table = table_fiche_etab()
#print(find("0860037Y", table))
#print(table_fiche_etab())
table = spe_tle()
print(find("0860037Y", table))
#statistica("0860037Y")
