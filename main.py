from fastapi import FastAPI
from pydantic import BaseModel

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

    return {
        "response": f"You asked: {user_message}"
    }