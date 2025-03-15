from flask import Flask, request

app = Flask(__name__)

@app.route('/envoie', methods=["POST"])
def envoie():

    if request.method == "POST":
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        qte = request.form.get("qte")


if __name__ == "__main__":
    app.run()
