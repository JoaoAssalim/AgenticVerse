from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class UserBaseModel(SQLModel):
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False)

class UserLoginModel(SQLModel):
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False)

class UserUpdateModel(SQLModel):
    name: Optional[EmailStr] | None = None
    email: Optional[str] | None = None
    password: Optional[str] | None = None

class UserResponseModel(SQLModel):
    id: str
    name: str
    email: str
    created_at: str
    updated_at: str