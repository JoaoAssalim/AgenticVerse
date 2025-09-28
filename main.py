from fastapi import FastAPI
from routers import agent

app = FastAPI()

app.include_router(agent.router)

@app.get("/health")
async def health():
    return {"message": "OK"}