from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# OEE Models
class OEEInput(BaseModel):
    availability: float = Field(..., ge=0, le=100, description="Availability percentage (0-100)")
    performance: float = Field(..., ge=0, le=100, description="Performance percentage (0-100)")
    quality: float = Field(..., ge=0, le=100, description="Quality percentage (0-100)")

class OEEResult(BaseModel):
    oee: float
    world_class: bool
    losses: dict
    recommendations: List[str]

# Process Step Model
class ProcessStep(BaseModel):
    name: str
    cycle_time: float = Field(..., gt=0, description="Cycle time in minutes")
    wait_time: float = Field(default=0, ge=0, description="Wait time in minutes")

# Chat Models
class Message(BaseModel):
    role: str  # user or assistant
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Conversation(BaseModel):
    id: str
    user_id: Optional[str] = None
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Document Models
class Document(BaseModel):
    id: Optional[str] = None
    content: str
    metadata: dict = {}
    embedding: Optional[List[float]] = None

class DocumentChunk(BaseModel):
    text: str
    metadata: dict
    chunk_index: int
