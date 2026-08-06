import json
import os

HISTORY_FILE = "history.json"


# -----------------------------
# Chat History
# -----------------------------
def load_history():

    if not os.path.exists(HISTORY_FILE):
        save_history([])

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        save_history([])
        return []


def save_history(history):

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )