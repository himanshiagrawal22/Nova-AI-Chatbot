import os
import shutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import uvicorn

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


# ============================================================
# APP
# ============================================================

app = FastAPI(title="Nova AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DIRECTORIES
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)


# ============================================================
# GLOBAL STATE
# ============================================================

history = load_history()

rag_index = None
rag_chunks = None
loaded_document = None


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Nova AI backend is running."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# LOAD PDF
# ============================================================

def load_pdf(pdf_name):

    global rag_index
    global rag_chunks
    global loaded_document

    pdf_path = os.path.join(DATA_DIR, pdf_name)

    # Build RAG index
    rag_index, rag_chunks = build_rag(pdf_path)

    loaded_document = pdf_name

    return f"📄 '{pdf_name}' loaded successfully."


# ============================================================
# REMOVE PDF
# ============================================================

def remove_pdf():

    global rag_index
    global rag_chunks
    global loaded_document

    rag_index = None
    rag_chunks = None
    loaded_document = None

    return "PDF removed successfully."


# ============================================================
# UPLOAD PDF API
# ============================================================

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    global loaded_document

    try:

        # ----------------------------------------------------
        # Check file exists
        # ----------------------------------------------------

        if not file:
            return {
                "success": False,
                "message": "No file uploaded."
            }

        # ----------------------------------------------------
        # Check extension
        # ----------------------------------------------------

        filename = file.filename

        if not filename.lower().endswith(".pdf"):

            return {
                "success": False,
                "message": "Only PDF files are allowed."
            }

        # ----------------------------------------------------
        # Save PDF
        # ----------------------------------------------------

        pdf_path = os.path.join(DATA_DIR, filename)

        with open(pdf_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # ----------------------------------------------------
        # Remove previous RAG
        # ----------------------------------------------------

        remove_pdf()

        # ----------------------------------------------------
        # Build new RAG
        # ----------------------------------------------------

        load_pdf(filename)

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return {
            "success": True,
            "filename": filename,
            "message": f"'{filename}' uploaded and loaded successfully."
        }

    except Exception as e:

        print("PDF UPLOAD ERROR:", e)

        return {
            "success": False,
            "message": str(e)
        }


# ============================================================
# REMOVE PDF API
# ============================================================

@app.delete("/remove-pdf")
def remove_pdf_api():

    global loaded_document

    try:

        old_document = loaded_document

        remove_pdf()

        # ----------------------------------------------------
        # Optionally delete physical PDF
        # ----------------------------------------------------

        if old_document:

            pdf_path = os.path.join(
                DATA_DIR,
                old_document
            )

            if os.path.exists(pdf_path):

                os.remove(pdf_path)

        return {
            "success": True,
            "message": "PDF removed successfully."
        }

    except Exception as e:

        print("REMOVE PDF ERROR:", e)

        return {
            "success": False,
            "message": str(e)
        }


# ============================================================
# STREAMING CHAT
# ============================================================

def process_message_stream(user_input):

    global history
    global rag_index
    global rag_chunks

    try:

        # ====================================================
        # MEMORY
        # ====================================================

        try:

            extracted = extract_memory(user_input)

            memory_service.update(extracted)

            long_term_memory = (
                memory_service.get_memory()
            )

        except Exception as e:

            print("MEMORY ERROR:", e)

            long_term_memory = ""


        # ====================================================
        # SAVE USER MESSAGE
        # ====================================================

        history.append({
            "role": "user",
            "content": user_input
        })

        save_history(history)


        # ====================================================
        # PDF / RAG MODE
        # ====================================================

        if rag_index is not None and rag_chunks is not None:

            print("Using PDF RAG...")

            reply = ask_pdf(
                user_input,
                rag_index,
                rag_chunks
            )

            if reply is None:

                reply = "I couldn't find an answer in the uploaded PDF."


            # ------------------------------------------------
            # Save assistant response
            # ------------------------------------------------

            history.append({
                "role": "assistant",
                "content": reply
            })

            save_history(history)


            # ------------------------------------------------
            # Send response
            # ------------------------------------------------

            yield reply

            return


        # ====================================================
        # NORMAL CHAT MODE
        # ====================================================

        print("Using normal Gemini chat...")


        prompt = build_prompt(
            history,
            long_term_memory
        )


        full_reply = ""


        # ====================================================
        # STREAM GEMINI RESPONSE
        # ====================================================

        for chunk in stream_gemini_generator(prompt):

            if chunk:

                full_reply += chunk

                yield chunk


        # ====================================================
        # SAVE ASSISTANT RESPONSE
        # ====================================================

        if full_reply:

            history.append({
                "role": "assistant",
                "content": full_reply
            })

            save_history(history)


    except Exception as e:

        print("CHAT ERROR:", e)

        yield "\n❌ Something went wrong. Please try again."


# ============================================================
# CHAT STREAM API
# ============================================================

@app.post("/chat/stream")
async def chat_stream(data: dict):

    message = data.get("message", "").strip()


    if not message:

        return StreamingResponse(
            iter(["Please enter a message."]),
            media_type="text/plain"
        )


    return StreamingResponse(
        process_message_stream(message),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("\n===================================")
    print("       NOVA AI BACKEND")
    print("===================================")
    print("Server starting...")
    print("API: http://127.0.0.1:8000")
    print("Docs: http://127.0.0.1:8000/docs")
    print("===================================\n")

    uvicorn.run(
    app,
    host="127.0.0.1",
    port=8000
)