from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import shutil

from nova import (
    process_message_stream,
    load_pdf,
    remove_pdf,
)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Nova AI API",
    description="Backend API for Nova AI",
    version="1.0.0",
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
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):
    message: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Nova AI Backend is Running 🚀"
    }


# ============================================================
# NORMAL CHAT
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # Use the streaming generator and combine chunks
        reply = ""

        for chunk in process_message_stream(request.message):
            reply += chunk

        return {
            "reply": reply
        }

    except Exception as e:

        print("CHAT ERROR:", e)

        return {
            "reply": "Sorry, something went wrong.",
            "error": str(e)
        }


# ============================================================
# STREAMING CHAT
# ============================================================

@app.post("/chat/stream")
def chat_stream(request: ChatRequest):

    try:

        return StreamingResponse(
            process_message_stream(request.message),
            media_type="text/plain"
        )

    except Exception as e:

        print("STREAM ERROR:", e)

        return {
            "error": str(e)
        }


# ============================================================
# UPLOAD PDF
# ============================================================

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    try:

        print("\n================================")
        print("PDF UPLOAD REQUEST")
        print("Filename:", file.filename)
        print("Content Type:", file.content_type)
        print("================================")

        # ----------------------------------------
        # Check file
        # ----------------------------------------

        if not file.filename:

            return {
                "success": False,
                "message": "No file selected."
            }

        if not file.filename.lower().endswith(".pdf"):

            return {
                "success": False,
                "message": "Only PDF files are allowed."
            }

        # ----------------------------------------
        # Create data directory
        # ----------------------------------------

        os.makedirs("data", exist_ok=True)

        # ----------------------------------------
        # Save PDF
        # ----------------------------------------

        pdf_path = os.path.join(
            "data",
            file.filename
        )

        with open(pdf_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        print("PDF saved at:", pdf_path)

        # ----------------------------------------
        # Build RAG index
        # ----------------------------------------

        result = load_pdf(file.filename)

        print("RAG RESULT:", result)

        # ----------------------------------------
        # Success
        # ----------------------------------------

        return {
            "success": True,
            "message": result,
            "filename": file.filename
        }

    except Exception as e:

        print("\n❌ PDF UPLOAD ERROR:")
        print(e)

        return {
            "success": False,
            "message": str(e)
        }


# ============================================================
# REMOVE PDF
# ============================================================

@app.delete("/remove-pdf")
def delete_pdf():

    try:

        result = remove_pdf()

        return {
            "success": True,
            "message": result
        }

    except Exception as e:

        print("REMOVE PDF ERROR:", e)

        return {
            "success": False,
            "message": str(e)
        }


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    print("\n======================================")
    print("          NOVA AI BACKEND")
    print("======================================")
    print("Server starting...")
    print("API:  http://127.0.0.1:8000")
    print("Docs: http://127.0.0.1:8000/docs")
    print("======================================\n")

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )