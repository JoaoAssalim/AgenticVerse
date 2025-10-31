from contextlib import asynccontextmanager
from fastapi import FastAPI

from routers import agent, users, integrations, auth
from database.config import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(agent.router)
app.include_router(users.router)
app.include_router(integrations.router)
app.include_router(auth.router)

@app.get("/health")
async def health():
    return {"message": "OK"}