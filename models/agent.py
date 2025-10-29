from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import Field, JSON
from sqlalchemy import Column

from sqlmodel import SQLModel


class AgentRequest(BaseModel):
    message: str


class AgentBaseModel(SQLModel):
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    system_prompt: str = Field(nullable=False)
    tools: List[str] = Field(sa_column=Column(JSON, nullable=False))
    provider: Optional[str] = Field(nullable=True)

class AgentUpdateModel(SQLModel):
    name: str | None = None
    description: str | None = None
    system_prompt: str | None = None
    tools: List[str] | None = None
    provider: str | None = None