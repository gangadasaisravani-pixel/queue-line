"""Request/response models for QueueLess Campus."""
from pydantic import BaseModel, Field


class QueueJoinRequest(BaseModel):
    student_name: str = Field(min_length=1, max_length=80, description="Student's name")
    service_id: int = Field(ge=1, le=3, description="1=Canteen, 2=Office, 3=Labs")


class QueueEntry(BaseModel):
    token: str
    student_name: str
    service_id: int
    position: int
    estimated_wait_minutes: int
    status: str = "waiting"
