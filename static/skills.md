# QueueLess Campus — Project Skill Guide

## Purpose
QueueLess Campus is a responsive, student-centered campus queue management web application designed for college canteens, administrative offices, and campus labs/services. It eliminates physical crowding by allowing students to join digital queues, receive instant tokens, track their position, and plan their wait time.

---

## File Architecture
- `main.py`: Core FastAPI application exposing RESTful API endpoints and serving static assets.
- `tools.py`: Utility functions for queue entry construction, queue listing, and wait-time estimation heuristics.
- `models.py`: Pydantic models for request validation (`QueueJoinRequest`) and data schemas (`QueueEntry`).
- `skill.md`: Comprehensive project guide, API documentation, and run instructions.
- `static/index.html`: Modern, responsive frontend dashboard built with accessible HTML, CSS, and vanilla JavaScript.

---

## Service IDs
- **1**: College Canteen (Category: Food)
- **2**: College Office (Category: Administration)
- **3**: Labs & Other Services (Category: Campus)

---

## How to Run Locally

1. From the project directory (`c:\Users\Sai Sravani\Desktop\open`), activate the virtual environment if applicable:
   ```powershell
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   ```
2. Start the FastAPI development server:
   ```powershell
   python -m uvicorn main:app --reload
   ```
3. Open the web app in your browser:
   - **Frontend UI**: [http://127.0.0.1:8000/static/index.html](http://127.0.0.1:8000/static/index.html)
   - **Interactive API Docs (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **Backend Status**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## API Endpoints Reference

### 1. `GET /`
Backend health check and welcome message.
- **Response**: `{"message": "QueueLess Campus backend is working!"}`

### 2. `GET /services`
Fetches all supported campus services with status and current waiting counts.
- **Response**:
  ```json
  {
    "services": [
      {
        "id": 1,
        "name": "College Canteen",
        "category": "Food",
        "status": "open",
        "total_waiting": 0
      },
      {
        "id": 2,
        "name": "College Office",
        "category": "Administration",
        "status": "open",
        "total_waiting": 0
      },
      {
        "id": 3,
        "name": "Labs & Other Services",
        "category": "Campus",
        "status": "open",
        "total_waiting": 0
      }
    ]
  }
  ```

### 3. `POST /join-queue`
Registers a student into a service queue and generates an incremental token.
- **Request Body** (`application/json`):
  ```json
  {
    "student_name": "Radha",
    "service_id": 1
  }
  ```
- **Success Response** (`200 OK`):
  ```json
  {
    "message": "Successfully joined the queue",
    "queue_entry": {
      "token": "Q001",
      "student_name": "Radha",
      "service_id": 1,
      "position": 1,
      "estimated_wait_minutes": 0,
      "status": "waiting"
    }
  }
  ```
- **Error Response** (`200 OK` or `422 Unprocessable Entity`):
  ```json
  {"error": "Invalid service ID"}
  ```

### 4. `GET /queue/{service_id}`
Returns all queued students for a particular service.
- **Parameters**: `service_id` (integer: 1, 2, or 3)
- **Response**:
  ```json
  {
    "service_id": 1,
    "total_waiting": 1,
    "queue": [
      {
        "token": "Q001",
        "student_name": "Radha",
        "service_id": 1,
        "position": 1,
        "estimated_wait_minutes": 0,
        "status": "waiting"
      }
    ]
  }
  ```

### 5. `GET /ask?question=...`
Campus assistance query endpoint (routes to local Ollama instance if configured).

---

## Technical Notes & Limitations

- **In-Memory Storage**: Queue state is maintained in Python dictionary memory (`queues = {1: [], 2: [], 3: []}`). All queue data and issued tokens reset whenever the server restarts.
- **Wait Time Heuristic**: Estimated wait times are derived from a simple arithmetic rule of thumb (`(position - 1) * 3` minutes). This is a fixed heuristic for planning purposes, not an AI prediction or live GPS tracking.
- **Future Enhancements**: For a full production rollout, consider integrating PostgreSQL / SQLite via SQLAlchemy, authentication via campus SSO/OAuth2, token cancellation, and WebSocket/SSE push notifications for live position updates.
