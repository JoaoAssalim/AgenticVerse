from sqlmodel import Field

from database.models.base import BaseModel

class UserModel(BaseModel, table=True):
    __tablename__ = "users"

    name: str = Field(nullable=False)
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)