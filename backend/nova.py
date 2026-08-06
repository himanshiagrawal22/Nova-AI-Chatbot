import os

from memory import (
    load_history,
    save_history,
)

from services.memory_service import memory_service

from memory_ai import extract_memory

from chatbot import (
    build_prompt,
    stream_gemini_generator,
)

from rag.rag_pipeline import (
    build_rag,
    ask_pdf,
)

# ----------------------------------------
# Global State
# ----------------------------------------

history = load_history()

rag_index = None
rag_chunks = None
loaded_document = None


# ----------------------------------------
# Load PDF
# ----------------------------------------

def load_pdf(pdf_name):

    global rag_index
    global rag_chunks
    global loaded_document

    pdf_path = os.path.join("data", pdf_name)

    rag_index, rag_chunks = build_rag(pdf_path)

    loaded_document = pdf_name

    return f"📄 '{pdf_name}' loaded successfully."


# ----------------------------------------
# Streaming Chat
# ----------------------------------------

def process_message_stream(user_input):

    global history
    global rag_index
    global rag_chunks

    # ----------------------------
    # Update Memory
    # ----------------------------

    extracted = extract_memory(user_input)

    memory_service.update(extracted)

    long_term_memory = memory_service.get_memory()

    # ----------------------------
    # Save User Message
    # ----------------------------

    history.append({
        "role": "user",
        "content": user_input
    })

    save_history(history)

    # ----------------------------
    # RAG
    # ----------------------------

    if rag_index is not None:

        reply = ask_pdf(
            user_input,
            rag_index,
            rag_chunks
        )

        history.append({
            "role": "assistant",
            "content": reply
        })

        save_history(history)

        yield reply
        return

    # ----------------------------
    # Build Prompt
    # ----------------------------

    prompt = build_prompt(
        history,
        long_term_memory
    )

    print("\n========== PROMPT ==========\n")
    print(prompt)
    print("\n============================\n")

    full_reply = ""

    for chunk in stream_gemini_generator(prompt):

        full_reply += chunk

        yield chunk

    history.append({
        "role": "assistant",
        "content": full_reply
    })

    save_history(history)