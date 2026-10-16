"""Utility functions for QueueLess Campus."""
from typing import Dict, List


def estimate_wait_minutes(position: int, minutes_per_person: int = 3) -> int:
    """Return a simple estimated wait time. This is a heuristic, not AI."""
    if position < 1:
        return 0
    return (position - 1) * max(1, minutes_per_person)


def make_queue_entry(token: str, student_name: str, service_id: int, position: int) -> Dict:
    """Build a consistent queue entry record."""
    return {
        "token": token,
        "student_name": student_name,
        "service_id": service_id,
        "position": position,
        "estimated_wait_minutes": estimate_wait_minutes(position),
        "status": "waiting",
    }


def list_service_queues(queues: Dict[int, List[dict]], service_id: int) -> List[dict]:
    """Return a copy of a service's current queue."""
    return list(queues.get(service_id, []))
