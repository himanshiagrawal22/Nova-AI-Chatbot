import json
from config import client, MODEL_NAME


def clean_json(text):
    """
    Remove Markdown code fences if Gemini returns them.
    """

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return text.strip()


def extract_memory(user_input):
    """
    Extract long-term facts about the user.
    """

    prompt = f"""
You are an AI memory extraction engine.

Your ONLY job is to extract important long-term facts about the USER.

Return ONLY valid JSON.

The JSON format MUST be:

{{
    "facts": [
        "fact 1",
        "fact 2"
    ]
}}

Rules:

1. Return ONLY JSON.
2. Never explain anything.
3. Never use Markdown.
4. Extract ONLY long-term information.
5. Ignore temporary information.
6. If there is nothing important, return:

{{"facts":[]}}

Examples:

User:
My name is Jarvis.

Output:
{{
    "facts":[
        "User's name is Jarvis."
    ]
}}

User:
I work as a software developer.

Output:
{{
    "facts":[
        "User works as a software developer."
    ]
}}

User:
I am learning SAP ABAP.

Output:
{{
    "facts":[
        "User is learning SAP ABAP."
    ]
}}

User:
I want to become an AI Engineer.

Output:
{{
    "facts":[
        "User wants to become an AI Engineer."
    ]
}}

User:
I like cricket and football.

Output:
{{
    "facts":[
        "User likes cricket.",
        "User likes football."
    ]
}}

User:
I live in Delhi.

Output:
{{
    "facts":[
        "User lives in Delhi."
    ]
}}

User:
Today I ate pizza.

Output:
{{"facts":[]}}

Now extract memory.

User:
{user_input}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    try:
        text = clean_json(response.text)

        memory = json.loads(text)

        if "facts" not in memory:
            memory["facts"] = []

        return memory

    except Exception as e:
        print("Memory Parsing Error:", e)
        return {"facts": []}