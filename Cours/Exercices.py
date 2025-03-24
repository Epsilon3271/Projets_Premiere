LIVRE = [
{"IDL":162, "TITRE":"Fondation", "AUTEUR":"Asimov"},
{"IDL":261, "TITRE":"Poemes", "AUTEUR":"Bonnefoy"},
{"IDL":179, "TITRE":"Kyoto", "AUTEUR":"Kawabata"},
{"IDL":284, "TITRE":"Planches courbes", "AUTEUR":"Bonnefoy"},
{"IDL":283, "TITRE":"Trilogie", "AUTEUR":"Mahfouz"}
         ]

ABONNE = [
{"IDA":27, "NOM": "Rita", "AGE": 16,"NBE" :10},
{"IDA":29, "NOM": "Riton", "AGE": 16,"NBE" :10},
{"IDA":33, "NOM": "Jules", "AGE": 17,"NBE" :10}
]

EMPRUNT = [
{"IDE":261, "IDA":27, "ANNEE":2021},
{"IDE":179, "IDA":29, "ANNEE":2021},
{"IDE":283, "IDA":27, "ANNEE":2021},
]
def afficher_table(table):
    for i in range(len(table)):
        ligne = ""
        for key in table[i].keys():
            ligne += f"{key} : {table[i][key]} | "
        print(ligne)
def identifier_livre(auteur):
    table =[]
    for i in range(len(LIVRE)):
        if LIVRE[i]["AUTEUR"] == str(auteur):
            table.append(LIVRE[i])
    return table
def livre_ida_annee(emprunteur):
    for i in range(len(EMPRUNT)):





#afficher_table(ABONNE)
afficher_table(identifier_livre("Kawabata"))
#print(ABONNE[1]["IDA"])