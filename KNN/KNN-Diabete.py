from csv import DictReader
import matplotlib.pyplot as plt
import math
def importation_data(fichier):
    with open(fichier, encoding="utf-8-sig") as f:
        return list(DictReader(f, delimiter=','))

def data():
    table_init = importation_data("C:/Users/shcor/PycharmProjects/Projets_Premiere/KNN/diabetes.csv")
    n = math.ceil(len(table_init) * 0.75)
    data = table_init[:n]
    return data

def test_data():
    table_init = importation_data("C:/Users/shcor/PycharmProjects/Projets_Premiere/KNN/diabetes.csv")
    n = math.ceil(len(table_init) * 0.75)
    data = table_init[n:]
    return data

def knn(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age,n):
    knn = []
    somme =0
    db = data()
    for i in range(len(db)):
        distance = (
            (int(Pregnancies) - int(db[i]["Pregnancies"]))**2 +
            (float(Glucose) - float(db[i]["Glucose"]))**2 +
            (float(BloodPressure) - float(db[i]["BloodPressure"]))**2 +
            (float(SkinThickness) - float(db[i]["SkinThickness"]))**2 +
            (float(Insulin) - float(db[i]["Insulin"]))**2 +
            (float(BMI) - float(db[i]["BMI"]))**2 +
            (float(DiabetesPedigreeFunction) - float(db[i]["DiabetesPedigreeFunction"]))**2 +
            (int(Age) - int(db[i]["Age"]))**2
        ) ** 0.5
        db[i]["distance"] = distance
        knn.append(db[i])
    #return sorted(knn, key=lambda d: d["distance"])
    knn = sorted(knn, key=lambda d: d["distance"])
    for i in range(n):
        somme += int(knn[i]["Outcome"])

    moyenne = somme / n

    if moyenne >= 0.5:
        prediction = 1
        probabilite = moyenne * 100
    else:
        prediction = 0
        probabilite = (1 - moyenne) * 100

    return prediction,round(probabilite, 2),knn[:n]

def evaluer_precision(epreuve, k_min, k_max):
    resultats = []

    for k in range(k_min, k_max + 1):
        bonnes_reponses = 0

        for ligne in epreuve:
            prediction, _, _ = knn(
                ligne["Pregnancies"],
                ligne["Glucose"],
                ligne["BloodPressure"],
                ligne["SkinThickness"],
                ligne["Insulin"],
                ligne["BMI"],
                ligne["DiabetesPedigreeFunction"],
                ligne["Age"],
                k
            )

            if prediction == int(ligne["Outcome"]):
                bonnes_reponses += 1

        precision = (bonnes_reponses / len(epreuve)) * 100
        resultats.append((k, precision))

    # # Tracé du graphique
    x = [r[0] for r in resultats]
    y = [r[1] for r in resultats]

    plt.plot(x, y, marker='o')
    plt.title("Précision en fonction du nombre de voisins (k)")
    plt.xlabel("Nombre de voisins (k)")
    plt.ylabel("Précision (%)")
    plt.grid(True)
    plt.show()

    return resultats
    #return sorted(resultats, key=lambda x: x[1], reverse=True)


print(evaluer_precision(test_data(),1, 20))
#print(knn(1,90,70,20,85,22.5,0.201,25,17))
