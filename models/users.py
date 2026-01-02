from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

class UserBaseModel(SQLModel):
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False)
    group: str = Field(nullable=False, default="user")

class UserLoginModel(SQLModel):
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False)

class UserUpdateModel(SQLModel):
    name: Optional[EmailStr] | None = None
    email: Optional[str] | None = None
    password: Optional[str] | None = None
    group: Optional[str] | None = None

class UserResponseModel(SQLModel):
    id: str
    name: str
    email: str
    created_at: str
    updated_at: str
    group: str