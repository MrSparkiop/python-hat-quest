import json

SAVE_FILE = "savefile.json"

def save_game(data):
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file)

def load_game():
    try:
        with open(SAVE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None
