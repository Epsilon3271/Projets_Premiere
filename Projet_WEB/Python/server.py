from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route('/envoie', methods=["POST"])
def envoie():
    nom = request.form.get("nom")
    prenom = request.form.get("prenom")
    qte = request.form.get("qte")
    day = request.form.get("menu")

    print(f"Nom: {nom}, Prénom: {prenom}, Quantité: {qte}, Jour:{day}")

    return jsonify({"message": "Données envoyées avec succès !"}), 200

if __name__ == "__main__":
    app.run(debug=True)
