from memory import load_history, save_history
from chatbot import build_prompt, stream_gemini

# Load Previous Chat
history = load_history()

print("=" * 60)
print("🤖 Gemini AI Chatbot")
print("Type 'exit' to quit.")
print("=" * 60)

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("\n👋 Goodbye!")
        break

    # Save User Message
    history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Build Prompt
    prompt = build_prompt(history)

    try:

        print("\nGemini: ", end="", flush=True)

        reply = stream_gemini(prompt)

        # Save Assistant Reply
        history.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        # Save Updated History
        save_history(history)

        print("-" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")