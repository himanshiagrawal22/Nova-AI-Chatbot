from config import client, MODEL_NAME
from prompts import SYSTEM_PROMPT

MAX_HISTORY = 10


def build_prompt(history, long_term_memory):
    """
    Build the prompt sent to Gemini.
    Includes:
    1. System Prompt
    2. Long-Term Memory
    3. Recent Chat History
    """

    prompt = f"{SYSTEM_PROMPT}\n\n"

    # -----------------------------
    # Long-Term Memory
    # -----------------------------
    facts = long_term_memory.get("facts", [])

    if facts:
        prompt += "Known facts about the user:\n"

        for fact in facts:
            prompt += f"- {fact}\n"

        prompt += "\n"

    # -----------------------------
    # Recent Chat History
    # -----------------------------
    prompt += "Conversation:\n"

    recent_history = history[-MAX_HISTORY:]

    for message in recent_history:
        prompt += (
            f"{message['role'].capitalize()}: "
            f"{message['content']}\n"
        )

    prompt += "Assistant:"

    # Uncomment while debugging
    # print("\n========== FINAL PROMPT ==========")
    # print(prompt)
    # print("==================================\n")

    return prompt


def stream_gemini(prompt):
    """
    Stream Gemini response token by token.
    """

    stream = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=prompt
    )

    full_response = ""

    for chunk in stream:

        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_response += chunk.text

    print()

    return full_response