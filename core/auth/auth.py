import uuid
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlmodel import Session, select

from database.config import engine
from database.models.users import UserModel

api_key = APIKeyHeader(name="x-api-key")

async def validate_api_key(api_key: str = Security(api_key)) -> UserModel:
    with Session(engine) as session:
        api_key_db = session.exec(select(UserModel).where(UserModel.api_key == uuid.UUID(api_key))).first()

        if not api_key_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

        return api_key_db

async def validate_api_key_websocket(api_key: str) -> UserModel:
    with Session(engine) as session:
        api_key_db = session.exec(select(UserModel).where(UserModel.api_key == uuid.UUID(api_key))).first()

        if not api_key_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

        return api_key_db