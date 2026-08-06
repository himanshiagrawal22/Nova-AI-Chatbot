import json
import os

from memory_ai import extract_memory

MEMORY_FILE = "long_term_memory.json"

DEFAULT_MEMORY = {
    "profile": {
        "name": "",
        "college": "",
        "cgpa": "",
        "email": "",
        "role": ""
    },
    "projects": [],
    "skills": [],
    "preferences": [],
    "goals": [],
    "notes": []
}


class MemoryService:

    def __init__(self):
        self.memory = self.load()

    def load(self):

        if not os.path.exists(MEMORY_FILE):

            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_MEMORY, f, indent=4)

        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=4, ensure_ascii=False)

    def get_memory(self):
        return self.memory

    def update_profile(self, profile):

        for key, value in profile.items():

            if value:
                self.memory["profile"][key] = value

    def merge_list(self, category, items):

        for item in items:

            if item and item not in self.memory[category]:
                self.memory[category].append(item)

    def update(self, user_input):
        print("\n================ USER INPUT ================")
        print(user_input)
        print("============================================")
        extracted = extract_memory(user_input)
        print("\n============= EXTRACTED MEMORY =============")
        print(extracted)
        print("============================================")
        self.update_profile(
            extracted.get("profile", {})
        )

        for category in [
            "projects",
            "skills",
            "preferences",
            "goals",
            "notes"
        ]:

            self.merge_list(
                category,
                extracted.get(category, [])
            )

        self.save()
        print("\n============= SAVED MEMORY =================")
        print(self.memory)
        print("============================================")
        return self.memory


memory_service = MemoryService()