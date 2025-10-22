from fastapi import FastAPI
from routers import agent
from routers import integrations
from database.config import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()

app.include_router(agent.router)
app.include_router(integrations.router)

@app.get("/health")
async def health():
    return {"message": "OK"}