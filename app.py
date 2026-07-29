from datetime import datetime
import os

from memory import (
    load_history,
    save_history,
    load_long_term_memory,
    save_long_term_memory
)

from chatbot import (
    build_prompt,
    stream_gemini
)

from memory_manager import (
    update_long_term_memory
)

from rag.rag_pipeline import (
    build_rag,
    ask_pdf
)

# ----------------------------------------
# Load Memory
# ----------------------------------------
history = load_history()
long_term_memory = load_long_term_memory()

# ----------------------------------------
# Loaded Document
# ----------------------------------------
rag_index = None
rag_chunks = None
loaded_document = None

print("=" * 50)
print("🤖 Nova AI")
print("Type 'exit' to quit.")
print("Type '/help' for commands.")
print("=" * 50)

while True:

    user_input = input("\nYou: ").strip()
    lower = user_input.lower()

    # ----------------------------------------
    # Exit
    # ----------------------------------------
    if lower == "exit":
        print("\n👋 Goodbye!")
        break

    # ----------------------------------------
    # Help
    # ----------------------------------------
    if lower == "/help":

        print("""
Available Commands

/help
/history
/clear
/save
exit

Load PDF naturally:

resume.pdf
notes.pdf
Open resume.pdf
Load notes.pdf

Close document
""")
        continue

    # ----------------------------------------
    # Detect PDF Automatically
    # ----------------------------------------
    pdf_name = None

    for word in user_input.split():

        if word.lower().endswith(".pdf"):
            pdf_name = word
            break

    if pdf_name:

        try:

            pdf_path = os.path.join(
                "data",
                pdf_name
            )

            rag_index, rag_chunks = build_rag(pdf_path)

            loaded_document = pdf_name

            print(f"\n📄 '{pdf_name}' loaded successfully.")
            print("You can now ask questions about this document.")

        except Exception as e:

            print(f"\n❌ {e}")

        continue

    # ----------------------------------------
    # Close Document
    # ----------------------------------------
    if lower in [
        "close document",
        "close pdf",
        "remove document",
        "unload pdf"
    ]:

        rag_index = None
        rag_chunks = None
        loaded_document = None

        print("\n📄 Document closed.")

        continue

    # ----------------------------------------
    # Clear History
    # ----------------------------------------
    if lower == "/clear":

        history.clear()
        save_history(history)

        print("\n✅ Chat history cleared.")

        continue

    # ----------------------------------------
    # Show History
    # ----------------------------------------
    if lower == "/history":

        print("\n📜 Chat History\n")

        if not history:

            print("No conversation found.")

        else:

            for message in history:

                print(
                    f"{message['role'].capitalize()}: "
                    f"{message['content']}"
                )

        print("\n" + "-" * 60)

        continue

    # ----------------------------------------
    # Save Conversation
    # ----------------------------------------
    if lower == "/save":

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        filename = f"chat_{timestamp}.txt"

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write("Nova AI Conversation\n")
            file.write("=" * 40 + "\n\n")

            if not history:

                file.write("No conversation available.\n")

            else:

                for message in history:

                    file.write(
                        f"{message['role'].capitalize()}: "
                        f"{message['content']}\n\n"
                    )

        print(f"\n✅ Conversation saved as '{filename}'")

        continue
        # ----------------------------------------
    # Update Long-Term Memory
    # ----------------------------------------
    long_term_memory = update_long_term_memory(
        user_input,
        long_term_memory
    )

    save_long_term_memory(
        long_term_memory
    )

    # ----------------------------------------
    # Save User Message
    # ----------------------------------------
    history.append({
        "role": "user",
        "content": user_input
    })

    # ----------------------------------------
    # Generate Response
    # ----------------------------------------
    print("\nNova: ", end="")

    # If a document is loaded, use RAG
    if rag_index is not None:

        reply = ask_pdf(
            user_input,
            rag_index,
            rag_chunks
        )

    # Otherwise use normal Gemini
    else:

        prompt = build_prompt(
            history,
            long_term_memory
        )

        reply = stream_gemini(prompt)

    # ----------------------------------------
    # Save Assistant Reply
    # ----------------------------------------
    history.append({
        "role": "assistant",
        "content": reply
    })

    save_history(history)

    print("\n" + "-" * 60)
