import uuid
from typing import List, Optional
from sqlmodel import Field, JSON, ForeignKey
from sqlalchemy import Column

from database.models.base import BaseModel

class AgentModel(BaseModel, table=True):
    __tablename__ = "agents"

    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    system_prompt: str = Field(nullable=False)
    tools: List[str] = Field(sa_column=Column(JSON, nullable=False))
    provider: Optional[str] = Field(nullable=True)
    user_id: uuid.UUID = ForeignKey("users.id")