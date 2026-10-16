
from fastapi import FastAPI
import requests

app = FastAPI(title="RescuePlate")

@app.get("/")
def read_root():
    return {"message": "RescuePlate backend is working!"}

@app.get("/ask")
def ask_ai(question: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:1b",
            "prompt": question,
            "stream": False
        },
        timeout=120
    )
    response.raise_for_status()
    return {
        "question": question,
        "answer": response.json()["response"]
    }
