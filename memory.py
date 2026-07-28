import json

FILE_NAME = "history.json"


def load_history():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_history(history):
    with open(FILE_NAME, "w") as file:
        json.dump(history, file, indent=4)