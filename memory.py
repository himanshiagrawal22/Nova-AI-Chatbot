import json

HISTORY_FILE = "history.json"
LONG_TERM_MEMORY_FILE = "long_term_memory.json"


# -----------------------------
# Chat History
# -----------------------------
def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


# -----------------------------
# Long-Term Memory
# -----------------------------
def load_long_term_memory():
    try:
        with open(LONG_TERM_MEMORY_FILE, "r") as file:
            memory = json.load(file)

            # Ensure correct format
            if "facts" not in memory:
                memory = {"facts": []}

            return memory

    except (FileNotFoundError, json.JSONDecodeError):
        return {"facts": []}


def save_long_term_memory(memory):
    with open(LONG_TERM_MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)