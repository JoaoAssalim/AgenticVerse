import os
from dotenv import load_dotenv

from sqlmodel import SQLModel, create_engine

from database.models import BaseModel, UserModel, AgentModel

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///agentic_system.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)