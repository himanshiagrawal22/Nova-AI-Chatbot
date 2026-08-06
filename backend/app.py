from fastapi import FastAPI
from fastapi import UploadFile, File
import shutil
import os

from nova import load_pdf
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from nova import process_message_stream

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Nova AI Backend is Running 🚀"
    }

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "success": False,
            "message": "Only PDF files are allowed."
        }

    os.makedirs("data", exist_ok=True)

    file_path = os.path.join("data", file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        message = load_pdf(file.filename)

        return {
            "success": True,
            "message": message,
            "filename": file.filename
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }


@app.post("/chat/stream")
def chat_stream(request: ChatRequest):

    return StreamingResponse(
        process_message_stream(request.message),
        media_type="text/plain"
    )