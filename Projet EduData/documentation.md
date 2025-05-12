# 🔍 Analyse complète du fonctionnement

Ce programme permet de visualiser les effectifs par spécialité dans les lycées généraux/polyvalents en France, à travers une **carte interactive** et des **graphiques Plotly** générés dynamiquement.

---

## Étapes du fonctionnement

### 1. Chargement des données
- Données importées depuis 3 CSV :
  - `geolocalisation.csv` (coordonnées)
  - `effectif_total.csv` (effectifs globaux)
  - `data_spe_1er.csv` et `data_spe_tle.csv` (spécialités)

### 2. Traitement
- **Filtrage** des établissements souhaités (non professionnels).
- **Fusion** des données géo + effectifs + infos administratives.
- Extraction des effectifs par spécialité et sexe.

### 3. Visualisation
- Création d’une carte Folium avec marqueurs.
- Génération des graphiques Plotly HTML au clic.

---

## Diagramme de fonctionnement général

```mermaid
flowchart TD
    A[Chargement CSV] --> B[Filtrage des lycées généraux]
    B --> C[Jointure géolocalisation + effectifs]
    C --> D[Création carte Folium]
    D --> E[Ajout de liens vers graphiques]
    C --> F[Filtrage par spécialité]
    F --> G[Création de graphiques Plotly]
````

---

## Algorigramme : `carte_create(...)`

```mermaid
graph TD
    Start([Début]) --> Load[Charger table_fiche_etab]
    Load --> Filter[Filtrer selon les critères]
    Filter --> Loop{Pour chaque établissement}
    Loop -->|Valide| Marker[Créer un marqueur sur la carte]
    Marker --> CallStats[Appeler statistica]
    CallStats --> NextLoop[Suivant]
    Loop -->|Invalide| NextLoop
    NextLoop --> End([Fin])
```

---

## Exemple de graphique généré

Un graphique HTML est généré automatiquement pour chaque établissement lorsqu'on clique sur son marqueur :

* Axe X : année scolaire
* Axe Y : effectif
* Lignes : Total / Filles / Garçons

---

## Résultat final

* Une carte interactive `carte.html`
* Des fichiers HTML pour chaque établissement (`graphiques_effectifs_UAI.html`)
* Une interface permettant d’explorer dynamiquement les données d'éducation.


