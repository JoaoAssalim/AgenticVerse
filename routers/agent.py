from fastapi import APIRouter

from core.api.agents import AgentsAPIView
from database.models.agent import AgentModel
from models.agent import AgentRequest, AgentBaseModel, AgentUpdateModel
from services.agent_orchestrator import OrchestratorAgent

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    responses={404: {"description": "Not found"}},
)

@router.post("/invoke")
def invoke_agent(request: AgentRequest):
    agent = OrchestratorAgent(request.params)
    response = agent.execute(request.prompt)
    return {"message": response}

@router.post("/create")
def create_agent(agent: AgentBaseModel):
    agent_model = agent.model_dump_json()
    agent_model = AgentModel.model_validate_json(agent_model)
    return AgentsAPIView().create_agent(agent_model)

@router.patch("/update/{agent_id}")
def update_agent(agent_id: str, agent: AgentUpdateModel):
    agent_model = agent.model_dump_json(exclude_unset=True)
    agent_model = AgentModel.model_validate_json(agent_model)
    return AgentsAPIView().update_agent(agent_id, agent_model)

@router.get("/get/{agent_id}")
def get_agent(agent_id: str):
    return AgentsAPIView().get_agent(agent_id)

@router.get("/get-all")
def get_all_agents():
    return AgentsAPIView().get_all_agents()

@router.delete("/delete/{agent_id}")
def delete_agent(agent_id: str):
    return AgentsAPIView().delete_agent(agent_id)