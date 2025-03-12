from flask import Flask, request

app = Flask(__name__)

def get_user_info(prenom, age, method):
    return f"""
    Vous avez envoyé une requête avec les données suivantes :
    <ul>
    <li>Prenom : {prenom}</li>
    <li>Age : {age}</li>
    </ul>
    En utilisant la méthode {method}
    <p>{prenom} est donc né en {int(2024) - int(age)}</p>
    """

@app.route('/envoie', methods=["GET", "POST"])
def envoie():
    if request.method == "GET":
        prenom = request.args.get("prenom")
        age = request.args.get("age")
        return get_user_info(prenom, age, request.method)

    elif request.method == "POST":
        prenom = request.form.get("prenom")
        age = request.form.get("age")
        return get_user_info(prenom, age, request.method)

if __name__ == "__main__":
    app.run()
