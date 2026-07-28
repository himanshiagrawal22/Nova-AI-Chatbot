from config import client, MODEL_NAME
from prompts import SYSTEM_PROMPT

def build_prompt(history):

    prompt = f"System:\n{SYSTEM_PROMPT}\n\n"

    for message in history:
        prompt += (
            f"{message['role'].capitalize()}: "
            f"{message['content']}\n"
        )

    return prompt


def stream_gemini(prompt):

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