from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests

try:
    from models import QueueJoinRequest
    from tools import make_queue_entry, list_service_queues
except ImportError:
    from static.models import QueueJoinRequest
    from static.tools import make_queue_entry, list_service_queues

app = FastAPI(title="QueueLess Campus")

# Enable CORS for external frontends (e.g. Vercel deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend from the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"message": "QueueLess Campus backend is working!"}


@app.get("/ask")
def ask_ai(question: str):
    """Optional AI endpoint for campus inquiries (requires local Ollama)."""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:1b",
            "prompt": question,
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    return {
        "question": question,
        "answer": response.json()["response"],
    }


# In-memory queue state. Note: resets when server restarts.
queues = {
    1: [],
    2: [],
    3: [],
}

next_token = 1


@app.get("/services")
def get_services():
    """Return the list of available campus services with current queue counts."""
    return {
        "services": [
            {
                "id": 1,
                "name": "College Canteen",
                "category": "Food",
                "status": "open",
                "total_waiting": len(queues.get(1, [])),
            },
            {
                "id": 2,
                "name": "College Office",
                "category": "Administration",
                "status": "open",
                "total_waiting": len(queues.get(2, [])),
            },
            {
                "id": 3,
                "name": "Labs & Other Services",
                "category": "Campus",
                "status": "open",
                "total_waiting": len(queues.get(3, [])),
            },
        ]
    }


@app.post("/join-queue")
def join_queue(request: QueueJoinRequest):
    """Add a student to the chosen service queue and issue a token."""
    global next_token

    if request.service_id not in queues:
        return {"error": "Invalid service ID"}

    cleaned_name = request.student_name.strip()
    if not cleaned_name:
        return {"error": "Student name cannot be empty"}

    token = f"Q{next_token:03d}"
    position = len(queues[request.service_id]) + 1

    queue_entry = make_queue_entry(
        token=token,
        student_name=cleaned_name,
        service_id=request.service_id,
        position=position,
    )

    queues[request.service_id].append(queue_entry)
    next_token += 1

    return {
        "message": "Successfully joined the queue",
        "queue_entry": queue_entry,
    }


@app.get("/queue/{service_id}")
def get_queue(service_id: int):
    """Retrieve all waiting entries for a specific service queue."""
    if service_id not in queues:
        return {"error": "Invalid service ID"}

    service_queue = list_service_queues(queues, service_id)
    return {
        "service_id": service_id,
        "total_waiting": len(service_queue),
        "queue": service_queue,
    }
