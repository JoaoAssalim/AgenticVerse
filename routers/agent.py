from fastapi import APIRouter, Depends, HTTPException
from services.agent_orchestrator import OrchestratorAgent
from models.agent import AgentRequest

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    responses={404: {"description": "Not found"}},
)

@router.post("/invoke")
def invoke_agent(request: AgentRequest):

    agent = OrchestratorAgent()
    response = agent.execute(request.prompt)
    return {"message": response}
