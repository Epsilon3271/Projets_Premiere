from csv import DictReader
import folium
import plotly.graph_objects as pg
from plotly.subplots import make_subplots
import math
import re

def importation_data(fichier):
    with open(fichier, encoding="utf-8-sig") as f:
        return list(DictReader(f, delimiter=';'))

def return_keys(fichier):
    with open(fichier, encoding="utf-8-sig") as f:
        return next(DictReader(f, delimiter=';')).keys()

def table_geoloc():
    return [
        {"UAI": e["UAI"], "LAT": e["latitude"], "LONG": e["longitude"]}
        for e in importation_data('geolocalisation.csv')
        if ("LYCEE" in e["denomination_principale"]
            or "GENERAL" in e["denomination_principale"]
            or "POLYVALENT" in e["denomination_principale"])
        and "PROFESSIONNEL" not in e["denomination_principale"]
    ]

def table_effectifs():
    return [
        {"UAI": e["UAI"], "ANNEE": e["Rentrée scolaire"], "EFTOT": e["Nombre d'élèves"]}
        for e in importation_data("effectif_total.csv")
    ]

def table_fiche_etab():
    etablissement = importation_data("data_spe_1er.csv")
    geoc_dict = {e["UAI"]: {"LAT": e["LAT"], "LONG": e["LONG"]} for e in table_geoloc()}
    effectif_dict = {e["UAI"]: e["EFTOT"] for e in table_effectifs()}

    seen = set()
    result = []
    for e in etablissement:
        uai = e["UAI"]
        if uai not in seen and uai in geoc_dict:
            seen.add(uai)
            result.append({
                "UAI": uai,
                "DENO": e["DENOMINATION PRINCIPALE"],
                "NOM": e["PATRONYME"],
                "TYPE": e["SECTEUR"],
                "ACA": e["ACADEMIE"],
                "DEPA": e["DEPARTEMENT"],
                "VILLE": e["COMMUNE"],
                "LAT": geoc_dict[uai]["LAT"],
                "LONG": geoc_dict[uai]["LONG"],
                "EFTOT": effectif_dict.get(uai)
            })
    return result

def spe_data(filename, col_annee, col_tot, col_f, col_g):
    data = importation_data(filename)
    keys = list(data[0].keys())
    specialites = []

    for e in data:
        d = {
            "UAI": e["UAI"],
            "ANNEE": e[col_annee],
            "EFTOT": e[col_tot],
            "EFTOTF": e[col_f],
            "EFTOTG": e[col_g]
        }
        for k in keys[17:]:
            if e[k] not in ("0", ""):
                d[k] = e[k]
        specialites.append(d)

    return specialites

def spe_1er():
    return spe_data("data_spe_1er.csv", "RENTREE SCOLAIRE", "EFFECTIF TOTAL", "EFFECTIF TOTAL FILLES", "EFFECTIF TOTAL GARCONS")
def spe_tle():
    return spe_data("data_spe_tle.csv", "Rentrée scolaire", "Effectif total", "Effectif total filles", "Effectif total garçons")

def find(UAI, table):
    return [e for e in table if e['UAI'] == UAI]

def carte_create(nom, type, ville, academie, departement):
    carte = folium.Map(location=[48.8566, 2.3522], zoom_start=13, tiles="CartoDB dark_matter")
    etab = table_fiche_etab()

    for e in etab:
        if ((not nom or nom.upper() == e["NOM"])
            and (not type or type.upper() == e["TYPE"])
            and (not ville or ville.upper() == e["VILLE"])
            and (not academie or academie.upper() == e["ACA"])
            and (not departement or departement.upper() == e["DEPA"])):

            try:
                lat, lon = float(e["LAT"]), float(e["LONG"])
                statistica(e["UAI"])

                popup_html = f"""
                <b>{e['DENO']}</b><br>
                {e['NOM']}<br>
                <i>{e['VILLE']}</i><br>
                <a href="graphiques_effectifs_{e['UAI']}.html" target="_blank">Voir les données</a>
                """

                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=folium.Icon(color="gray", icon="university", prefix="fa")
                ).add_to(carte)
            except ValueError:
                print(f"Coordonnées invalides pour {e['UAI']}")
    carte.save("carte.html")
    return carte

def statistica(uai):
    # Récupération du nom de l'établissement
    nom = next((e["NOM"] for e in table_fiche_etab() if e["UAI"] == uai), "")

    pr = sorted(find(uai, spe_1er()), key=lambda x: x["ANNEE"])
    tle = sorted(find(uai, spe_tle()), key=lambda x: x["ANNEE"])

    # --- Première figure : Total/Filles/Garçons en 1ère et Terminale ---
    def get_traces(data):
        annees = [int(x["ANNEE"]) for x in data]
        tot = [int(x["EFTOT"]) for x in data]
        filles = [int(x["EFTOTF"]) for x in data]
        garcons = [int(x["EFTOTG"]) for x in data]
        return annees, tot, filles, garcons

    a_pr, t_pr, f_pr, g_pr = get_traces(pr)
    a_tle, t_tle, f_tle, g_tle = get_traces(tle)

    fig1 = make_subplots(rows=1, cols=2, subplot_titles=["Première", "Terminale"])

    fig1.add_trace(pg.Scatter(x=a_pr, y=t_pr, name='Total 1ère', line=dict(color='red')), row=1, col=1)
    fig1.add_trace(pg.Scatter(x=a_pr, y=f_pr, name='Filles 1ère', line=dict(color='hotpink')), row=1, col=1)
    fig1.add_trace(pg.Scatter(x=a_pr, y=g_pr, name='Garçons 1ère', line=dict(color='blue')), row=1, col=1)

    fig1.add_trace(pg.Scatter(x=a_tle, y=t_tle, name='Total Tle', line=dict(color='red')), row=1, col=2)
    fig1.add_trace(pg.Scatter(x=a_tle, y=f_tle, name='Filles Tle', line=dict(color='hotpink')), row=1, col=2)
    fig1.add_trace(pg.Scatter(x=a_tle, y=g_tle, name='Garçons Tle', line=dict(color='blue')), row=1, col=2)

    fig1.update_layout(
        title_text=f"Évolution des effectifs filles/garçons en première et terminale dans le lycée {nom}",
        showlegend=True
    )

    # --- Deuxième figure : par spécialité et genre en Première ---
    specialites_pr = sorted({
        key.replace(" - filles", "")
        for row in pr for key in row if key.endswith(" - filles")
    })

    n_pr = len(specialites_pr)
    cols = 2
    rows_pr = math.ceil(n_pr / cols)

    def couper_titre(titre, max_len=20):
        return "<br>".join([titre[i:i+max_len] for i in range(0, len(titre), max_len)])

    fig2 = make_subplots(
        rows=rows_pr,
        cols=cols,
        subplot_titles=[couper_titre(sp) for sp in specialites_pr]
    )

    for idx, specialite in enumerate(specialites_pr):
        annees, filles, garcons = [], [], []
        for row in pr:
            annees.append(row['ANNEE'])
            filles.append(int(row.get(f"{specialite} - filles", 0)))
            garcons.append(int(row.get(f"{specialite} - garçons", 0)))

        row_i = idx // cols + 1
        col_i = idx % cols + 1

        fig2.add_trace(pg.Scatter(
            x=annees, y=filles, mode='lines+markers', name='Filles',
            line=dict(color='deeppink'), showlegend=(idx == 0)
        ), row=row_i, col=col_i)

        fig2.add_trace(pg.Scatter(
            x=annees, y=garcons, mode='lines+markers', name='Garçons',
            line=dict(color='blue', dash='dash'), showlegend=(idx == 0)
        ), row=row_i, col=col_i)

    fig2.update_layout(
        height=300 * rows_pr,
        title_text="Spécialités en première",
        template='plotly_white',
        legend_title='Genre',
        margin=dict(t=80),
        font=dict(size=11),
    )
    fig2.update_annotations(font_size=10)

    # --- Troisième figure : combinaisons de spécialités en Terminale ---
    def nettoyer_specialite(code):
        return re.sub(r"^\d+\s*-\s*", "", code)

    specialites_tle = sorted({
        nettoyer_specialite(key.replace(" - filles", ""))
        for row in tle for key in row if key.endswith(" - filles")
    })

    n_tle = len(specialites_tle)
    rows_tle = math.ceil(n_tle / cols)

    fig3 = make_subplots(
        rows=rows_tle,
        cols=cols,
        subplot_titles=[couper_titre(sp) for sp in specialites_tle]
    )

    for idx, specialite in enumerate(specialites_tle):
        annees, filles, garcons = [], [], []
        for row in tle:
            annee = row['ANNEE']
            key_f = next((k for k in row if k.endswith(" - filles") and nettoyer_specialite(k.replace(" - filles", "")) == specialite), None)
            key_g = key_f.replace(" - filles", " - garcons") if key_f else None
            if key_f and key_g:
                filles.append(int(row.get(key_f, 0)))
                garcons.append(int(row.get(key_g, 0)))
                annees.append(annee)

        row_i = idx // cols + 1
        col_i = idx % cols + 1

        fig3.add_trace(pg.Scatter(
            x=annees, y=filles, mode='lines+markers', name='Filles',
            line=dict(color='deeppink'), showlegend=(idx == 0)
        ), row=row_i, col=col_i)

        fig3.add_trace(pg.Scatter(
            x=annees, y=garcons, mode='lines+markers', name='Garçons',
            line=dict(color='blue', dash='dash'), showlegend=(idx == 0)
        ), row=row_i, col=col_i)

    fig3.update_layout(
        height=300 * rows_tle,
        title_text="Spécialités en terminale",
        template='plotly_white',
        legend_title='Genre',
        margin=dict(t=80),
        font=dict(size=11),
    )
    fig3.update_annotations(font_size=10)

    # --- Export HTML combiné ---
    html1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')
    html2 = fig2.to_html(full_html=False, include_plotlyjs=False)
    html3 = fig3.to_html(full_html=False, include_plotlyjs=False)

    with open(f"graphiques_effectifs_{uai}.html", "w", encoding="utf-8") as f:
        f.write(f"""
        <html>
        <head><meta charset="utf-8"><title>Statistiques lycée {nom}</title></head>
        <body>
            {html1}
            <hr>
            {html2}
            <hr>
            {html3}
        </body>
        </html>
        """)

def UI_user():
    ascii_art = """
    EEEEEEEEEEEEEEEEEEEEEEDDDDDDDDDDDDD       UUUUUUUU     UUUUUUUU     DDDDDDDDDDDDD                  AAA         TTTTTTTTTTTTTTTTTTTTTTT         AAA               
    E::::::::::::::::::::ED::::::::::::DDD    U::::::U     U::::::U     D::::::::::::DDD              A:::A        T:::::::::::::::::::::T        A:::A              
    E::::::::::::::::::::ED:::::::::::::::DD  U::::::U     U::::::U     D:::::::::::::::DD           A:::::A       T:::::::::::::::::::::T       A:::::A             
    EE::::::EEEEEEEEE::::EDDD:::::DDDDD:::::D UU:::::U     U:::::UU     DDD:::::DDDDD:::::D         A:::::::A      T:::::TT:::::::TT:::::T      A:::::::A            
      E:::::E       EEEEEE  D:::::D    D:::::D U:::::U     U:::::U        D:::::D    D:::::D       A:::::::::A     TTTTTT  T:::::T  TTTTTT     A:::::::::A           
      E:::::E               D:::::D     D:::::DU:::::D     D:::::U        D:::::D     D:::::D     A:::::A:::::A            T:::::T            A:::::A:::::A          
      E::::::EEEEEEEEEE     D:::::D     D:::::DU:::::D     D:::::U        D:::::D     D:::::D    A:::::A A:::::A           T:::::T           A:::::A A:::::A         
      E:::::::::::::::E     D:::::D     D:::::DU:::::D     D:::::U        D:::::D     D:::::D   A:::::A   A:::::A          T:::::T          A:::::A   A:::::A        
      E:::::::::::::::E     D:::::D     D:::::DU:::::D     D:::::U        D:::::D     D:::::D  A:::::A     A:::::A         T:::::T         A:::::A     A:::::A       
      E::::::EEEEEEEEEE     D:::::D     D:::::DU:::::D     D:::::U        D:::::D     D:::::D A:::::AAAAAAAAA:::::A        T:::::T        A:::::AAAAAAAAA:::::A      
      E:::::E               D:::::D     D:::::DU:::::D     D:::::U        D:::::D     D:::::DA:::::::::::::::::::::A       T:::::T       A:::::::::::::::::::::A     
      E:::::E       EEEEEE  D:::::D    D:::::D U::::::U   U::::::U        D:::::D    D:::::DA:::::AAAAAAAAAAAAA:::::A      T:::::T      A:::::AAAAAAAAAAAAA:::::A    
    EE::::::EEEEEEEE:::::EDDD:::::DDDDD:::::D  U:::::::UUU:::::::U      DDD:::::DDDDD:::::DA:::::A             A:::::A   TT:::::::TT   A:::::A             A:::::A   
    E::::::::::::::::::::ED:::::::::::::::DD    UU:::::::::::::UU       D:::::::::::::::DDA:::::A               A:::::A  T:::::::::T  A:::::A               A:::::A  
    E::::::::::::::::::::ED::::::::::::DDD        UU:::::::::UU         D::::::::::::DDD A:::::A                 A:::::A T:::::::::T A:::::A                 A:::::A 
    EEEEEEEEEEEEEEEEEEEEEEDDDDDDDDDDDDD             UUUUUUUUU           DDDDDDDDDDDDD   AAAAAAA                   AAAAAAATTTTTTTTTTTAAAAAAA                   AAAAAAA
    """

    print(ascii_art)
    print("Bienvenue sur Edu Data")
    print("\nVeuillez renseigner les critères de recherche pour filtrer les lycées.")
    print("Laissez vide un champ si vous ne souhaitez pas filtrer dessus.")

    nom = input("Nom (patronyme) de l’établissement : ").strip()
    type_etab = input("Type (PUBLIC ou PRIVE) : ").strip()
    ville = input("Ville : ").strip()
    academie = input("Académie : ").strip()
    departement = input("Département (n° ou nom) : ").strip()

    print("\nGénération de la carte en cours...")
    carte_create(nom if nom else None,
                 type_etab if type_etab else None,
                 ville if ville else None,
                 academie if academie else None,
                 departement if departement else None)
    print("Carte générée et enregistrée sous le nom 'carte.html'.")

if __name__ == "__main__":
    UI_user()




