from fastapi import FastAPI
from routers import agent
from routers import integrations

app = FastAPI()

app.include_router(agent.router)
app.include_router(integrations.router)

@app.get("/health")
async def health():
    return {"message": "OK"}