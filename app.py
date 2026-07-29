from datetime import datetime

from memory import (
    load_history,
    save_history,
    load_long_term_memory,
    save_long_term_memory
)

from chatbot import build_prompt, stream_gemini
from memory_manager import update_long_term_memory

# -----------------------------
# Load previous chat history
# -----------------------------
history = load_history()

# -----------------------------
# Load long-term memory
# -----------------------------
long_term_memory = load_long_term_memory()

print("=" * 50)
print("🤖 Nova AI Chatbot")
print("Type 'exit' to quit.")
print("Type '/help' for available commands.")
print("=" * 50)

while True:

    user_input = input("\nYou: ")

    # -----------------------------
    # Exit chatbot
    # -----------------------------
    if user_input.lower() == "exit":
        print("\n👋 Goodbye!")
        break

    # -----------------------------
    # /help Command
    # -----------------------------
    if user_input == "/help":
        print("""
📖 Available Commands

/help      Show all commands
/clear     Clear chat history
/history   Show previous conversation
/save      Save conversation
""")
        continue

    # -----------------------------
    # /clear Command
    # -----------------------------
    if user_input == "/clear":
        history.clear()
        save_history(history)

        print("✅ Chat history cleared.")
        continue

    # -----------------------------
    # /history Command
    # -----------------------------
    if user_input == "/history":

        print("\n📜 Chat History\n")

        if not history:
            print("No conversation found.")
        else:
            for message in history:
                print(f"{message['role'].capitalize()}: {message['content']}")

        print("\n" + "-" * 60)
        continue

    # -----------------------------
    # /save Command
    # -----------------------------
    if user_input == "/save":

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"chat_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as file:

            file.write("Nova AI Chatbot Conversation\n")
            file.write("=" * 40 + "\n\n")

            if not history:
                file.write("No conversation available.\n")
            else:
                for message in history:
                    file.write(
                        f"{message['role'].capitalize()}: {message['content']}\n\n"
                    )

        print(f"✅ Conversation saved as '{filename}'")
        continue

    # -----------------------------
    # Update Long-Term Memory
    # -----------------------------
    long_term_memory = update_long_term_memory(
        user_input,
        long_term_memory
    )

    save_long_term_memory(long_term_memory)

    # -----------------------------
    # Save user message
    # -----------------------------
    history.append({
        "role": "user",
        "content": user_input
    })

    # -----------------------------
    # Build Prompt
    # -----------------------------
    prompt = build_prompt(
        history,
        long_term_memory
    )

    print("\nNova: ", end="")

    # -----------------------------
    # Get AI Response
    # -----------------------------
    reply = stream_gemini(prompt)

    # -----------------------------
    # Save Assistant Reply
    # -----------------------------
    history.append({
        "role": "assistant",
        "content": reply
    })

    # -----------------------------
    # Save Chat History
    # -----------------------------
    save_history(history)

    print("\n" + "-" * 60)