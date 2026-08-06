import json
from config import client, MODEL_NAME


def clean_json(text):
    text = text.replace("```json", "")
    text = text.replace("```", "")
    return text.strip()


import json
from config import client, MODEL_NAME


def clean_json(text):
    text = text.replace("```json", "")
    text = text.replace("```", "")
    return text.strip()


def extract_memory(user_input):

    prompt = f"""
You are Nova's memory extraction engine.

Your job is to extract ONLY long-term user information.

Return ONLY valid JSON.

Schema:

{{
  "profile": {{
      "name": "",
      "college": "",
      "cgpa": "",
      "email": "",
      "role": ""
  }},
  "projects": [],
  "skills": [],
  "preferences": [],
  "goals": [],
  "notes": []
}}

IMPORTANT RULES

1. If the user says:
- I am ...
- My name is ...
- Call me ...

then UPDATE the name.

Example:

User:
I am Rimjhim

Output:

{{
  "profile": {{
      "name": "Rimjhim"
  }},
  "projects": [],
  "skills": [],
  "preferences": [],
  "goals": [],
  "notes": []
}}

2. If the user gives a new college, role, CGPA or email,
return the NEW value.

3. Never keep old values.

4. Unknown fields should remain empty.

5. Arrays should contain only new information.

6. Return ONLY JSON.

User:

{user_input}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    print("\n========== GEMINI MEMORY ==========")
    print(response.text)
    print("===================================\n")

    try:

        memory = json.loads(clean_json(response.text))

        memory.setdefault("profile", {})
        memory.setdefault("projects", [])
        memory.setdefault("skills", [])
        memory.setdefault("preferences", [])
        memory.setdefault("goals", [])
        memory.setdefault("notes", [])

        return memory

    except Exception as e:

        print(e)

        return {
            "profile": {},
            "projects": [],
            "skills": [],
            "preferences": [],
            "goals": [],
            "notes": []
        }