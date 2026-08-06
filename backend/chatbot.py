from config import client, MODEL_NAME
from prompts import SYSTEM_PROMPT

MAX_HISTORY = 10


def build_prompt(history, long_term_memory):
    prompt = f"{SYSTEM_PROMPT}\n\n"

    # -----------------------------
    # Long-Term Memory
    # -----------------------------
    prompt += "Known information about the user:\n"

    profile = long_term_memory.get("profile", {})

    for key, value in profile.items():
        if value:
            prompt += f"{key.capitalize()}: {value}\n"

    for category in [
        "projects",
        "skills",
        "preferences",
        "goals",
        "notes",
    ]:

        items = long_term_memory.get(category, [])

        if items:
            prompt += f"\n{category.capitalize()}:\n"

            for item in items:
                prompt += f"- {item}\n"

    prompt += "\n"

    # -----------------------------
    # Recent Conversation
    # -----------------------------
    prompt += "Conversation:\n"

    recent_history = history[-MAX_HISTORY:]

    for message in recent_history:
        prompt += (
            f"{message['role'].capitalize()}: "
            f"{message['content']}\n"
        )

    prompt += "Assistant:"

    return prompt


def stream_gemini(prompt):
    stream = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=prompt,
    )

    full_response = ""

    for chunk in stream:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_response += chunk.text

    print()

    return full_response


def stream_gemini_generator(prompt):
    stream = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=prompt,
    )

    for chunk in stream:
        if chunk.text:
            yield chunk.text