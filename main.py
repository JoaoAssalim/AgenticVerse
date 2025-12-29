import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from database.config import create_db_and_tables
from routers import agent, users, integrations, auth, rag

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(agent.router)
app.include_router(users.router)
app.include_router(integrations.router)
app.include_router(auth.router)
app.include_router(rag.router)

@app.get("/health")
async def health():
    return {"message": "OK"}