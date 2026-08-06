from dotenv import load_dotenv
import os
from google import genai

# Load environment variables
load_dotenv()

# Create Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Gemini Model
MODEL_NAME = "gemini-3.1-flash-lite"