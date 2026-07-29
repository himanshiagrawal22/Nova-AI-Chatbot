import json
import os

HISTORY_FILE = "history.json"
LONG_TERM_MEMORY_FILE = "long_term_memory.json"


# -----------------------------
# Chat History
# -----------------------------
def load_history():

    # Create file if it doesn't exist
    if not os.path.exists(HISTORY_FILE):
        save_history([])

    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        save_history([])
        return []


def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


# -----------------------------
# Long-Term Memory
# -----------------------------
def load_long_term_memory():

    # Create file if it doesn't exist
    if not os.path.exists(LONG_TERM_MEMORY_FILE):
        save_long_term_memory({"facts": []})

    try:
        with open(LONG_TERM_MEMORY_FILE, "r") as file:
            memory = json.load(file)

            # Ensure correct format
            if not isinstance(memory, dict):
                memory = {"facts": []}

            if "facts" not in memory:
                memory["facts"] = []

            return memory

    except json.JSONDecodeError:
        save_long_term_memory({"facts": []})
        return {"facts": []}


def save_long_term_memory(memory):
    with open(LONG_TERM_MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)