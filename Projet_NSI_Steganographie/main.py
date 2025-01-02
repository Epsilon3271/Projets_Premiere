from Projet_Steganographie_Encodage import hide_msg
from Projet_NSI_Steganographie_Decode import decode

import time

def aide(commande=None):
    """
    Affiche toutes les commandes ou les spécification d'une commande si commande est spécifié
    """

    if commande is None:
        for el in COMMANDS:
            print(f"{el} | {COMMANDS[el]["description"]}")
    else:
        print(commande.upper())
        print("".join(["-" for _ in range(len(commande))]))
        print(COMMANDS[commande]["description"])
        print(f"EXEMPLE \n {commande} {" | ".join(COMMANDS[commande]["arguments"][0:-1])} {"| ("+COMMANDS[commande]["arguments"][-1]+")" if COMMANDS[commande]["arguments"][-1] is not None else " "}")

    return " "

COMMANDS = {
    "decode": {"description": "Affiche le message caché dans une image.",
               "arguments": ["chemin d'accès à l'image contenant le message caché", None],
               "fonction": decode},
    "encode": {"description": "Enregistre une image contenant un message caché.",
               "arguments": ["message à cacher", "chemin d'accès à l'image d'origine", "nom de la nouvelle image"], # La dernière information est considérée comme ooptionnelle
               "fonction": hide_msg},
    "aide": {"description": "Affiche toutes les commandes.",
             "arguments": ["nom de la commande"],
             "fonction": aide},
    "quit": {"description": "Stoppe le programme",
             "arguments": [],
             "fonction": quit}
}

texte = """
    ·········································
    : ______   ______ ______   ______ _____ :
    :|  _ \ \ / / ___|  _ \ \ / /  _ \_   _|:
    :| |_) \ V / |   | |_) \ V /| |_) || |  :
    :|  __/ | || |___|  _ < | | |  __/ | |  :
    :|_|    |_| \____|_| \_\|_| |_|    |_|  :
    ·········································
    """

for char in texte:
    print(char, end='', flush=True)  # Affiche un caractère sans retour à la ligne
    time.sleep(0.010)  # Ajustez la durée pour contrôler la vitesse

while True:
    com = input("user > ")

    # Couper la commands
    result = []
    current = ""
    value = False

    for car in com:
        if car == '"':
            value = not value
            continue

        if car == " " and not value:
            result.append(current)
            current = ""
            continue

        current += car

    result.append(current)
    com = result

    if not com[0] in COMMANDS:
        print("Commande non existante. Tapez `aide` pour plus d'information.")
        continue
    
    args = [None for _ in COMMANDS[com[0]]["arguments"]]

    if len(com) == 2 and not COMMANDS[com[0]]["arguments"][-1] is None:
        args[-1] = com[1]
            
    elif len(com) - 1 > len(args):
        print("Trop d'arguments ont été données. Tapez `aide commande` pour plus d'informations.")
        continue

    for i in range(1, len(com)):
        args[i-1] = com[i]
    
    for i in range(len(args)):
        if not args[i] is None:
            continue
        if i == len(args) - 1:
            args = args[0:-1]
            continue
        args[i] = input(f"Entrez le {COMMANDS[com[0]]["arguments"][i]} : ")

    print(COMMANDS[com[0]]["fonction"](*args))