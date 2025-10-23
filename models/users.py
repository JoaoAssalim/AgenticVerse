from re import S
from typing import Optional
from sqlmodel import Field

from sqlmodel import SQLModel

class UserBaseModel(SQLModel):
    name: str = Field(nullable=False)
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)

class UserUpdateModel(SQLModel):
    name: Optional[str] | None = None
    email: Optional[str] | None = None
    password: Optional[str] | None = None

class UserResponseModel(SQLModel):
    id: str
    name: str
    email: str
    created_at: str
    updated_at: str