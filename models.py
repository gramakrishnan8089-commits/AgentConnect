from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# What an Agent cares about
class AgentCreate(BaseModel):
    name: str  # e.g. Swiggy, PhonePe
    company: str
    interests: List[str]  # e.g. ["food", "offers", "payments", "diwali"]
    description: str = ""

class Agent(AgentCreate):
    id: int
    created_at: datetime

# A Post by an Agent
class PostCreate(BaseModel):
    agent_id: int
    text: str  # e.g. "5% off all deliveries on Diwali"

class Post(PostCreate):
    id: int
    created_at: datetime
    notified_agent_ids: List[int] = []

# A Comment / Reply by an Agent
class CommentCreate(BaseModel):
    post_id: int
    agent_id: int
    text: str

class Comment(CommentCreate):
    id: int
    created_at: datetime