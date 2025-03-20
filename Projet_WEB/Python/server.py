from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/envoie', methods=["POST"])
def envoie():
    nom = request.form.get("nom")
    prenom = request.form.get("prenom")
    qte = request.form.get("qte")

    print(f"Nom: {nom}, Prénom: {prenom}, Quantité: {qte}")

    return jsonify({"message": "Données envoyées avec succès !"}), 200

if __name__ == "__main__":
    app.run(debug=True)
