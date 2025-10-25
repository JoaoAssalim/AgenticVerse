import uuid
from sqlmodel import Field

from database.models.base import BaseModel

class UserModel(BaseModel, table=True):
    __tablename__ = "users"

    name: str = Field(nullable=False)
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)
    api_key: uuid.UUID = Field(default_factory=uuid.uuid4, nullable=True)
    is_active: bool = Field(default=True, nullable=True)