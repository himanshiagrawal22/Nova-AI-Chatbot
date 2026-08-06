from fastapi import FastAPI
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


@app.post("/chat/stream")
def chat_stream(request: ChatRequest):

    return StreamingResponse(
        process_message_stream(request.message),
        media_type="text/plain"
    )