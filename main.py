from fastapi import FastAPI
from pydantic import BaseModel
import ollama

app = FastAPI()


# -----------------------------
# Home Route
# -----------------------------
@app.get("/")
def home():
    return {"status": "CloveToolBot Backend Running"}


# -----------------------------
# Request Model
# -----------------------------
class ChatRequest(BaseModel):
    message: str


# -----------------------------
# Chat Route
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    user_message = request.message

    # Send message to Ollama
    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "system",
                "content": "You are CloveToolBot, an AI assistant for BIM, construction, surveying, GIS, digital construction, architecture, engineering, and infrastructure workflows."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    ai_response = response["message"]["content"]

    return {
        "response": ai_response
    }