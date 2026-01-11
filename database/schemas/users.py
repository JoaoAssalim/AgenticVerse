import uuid
from sqlmodel import Field

from database.schemas import BaseModel

class UserModel(BaseModel, table=True):
    __tablename__ = "users"

    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    api_key: uuid.UUID = Field(default_factory=uuid.uuid4, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    group: str = Field(default_factory="user", nullable=True) # user, manager, admin