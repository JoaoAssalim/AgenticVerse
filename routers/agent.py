from fastapi import APIRouter, Depends, HTTPException
from services.artificial_intelligence import AgentModel

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    responses={404: {"description": "Not found"}},
)

@router.post("/invoke")
def invoke_agent(prompt: str):

    agent = AgentModel()
    response = agent.invoke(prompt)
    return {"message": response}
