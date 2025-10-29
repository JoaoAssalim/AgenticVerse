from fastapi import APIRouter, Depends, Header
from typing import Annotated

from core.api.agents import AgentsAPIView
from database.models.agent import AgentModel
from models.agent import AgentRequest, AgentBaseModel, AgentUpdateModel
from services.agent_orchestrator import OrchestratorAgent
from core.auth.auth import validate_api_key
from database.models.users import UserModel
from models.headers import CommonHeaders

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    responses={404: {"description": "Not found"}},
)

@router.post("/invoke")
def invoke_agent(request: AgentRequest, header: Annotated[CommonHeaders, Header()], user: UserModel = Depends(validate_api_key)):
    agent_id = header.agent_id
    agent = AgentsAPIView().get_agent(agent_id, user.id)

    agent = OrchestratorAgent(agent)
    response = agent.execute(request.message)
    return {"message": response}

@router.post("/create")
def create_agent(agent: AgentBaseModel, user: UserModel = Depends(validate_api_key)):
    agent_model = agent.model_dump_json()
    agent_model = AgentModel.model_validate_json(agent_model)
    return AgentsAPIView().create_agent(agent_model, user.id)

@router.patch("/update/{agent_id}")
def update_agent(agent_id: str, agent: AgentUpdateModel, user: UserModel = Depends(validate_api_key)):
    agent_model = agent.model_dump_json(exclude_unset=True)
    agent_model = AgentModel.model_validate_json(agent_model)
    return AgentsAPIView().update_agent(agent_id, agent_model, user.id)

@router.get("/get/{agent_id}")
def get_agent(agent_id: str, user: UserModel = Depends(validate_api_key)):
    return AgentsAPIView().get_agent(agent_id, user.id)

@router.get("/get-all")
def get_all_agents(user: UserModel = Depends(validate_api_key)):
    return AgentsAPIView().get_all_agents(user.id)

@router.delete("/delete/{agent_id}")
def delete_agent(agent_id: str, user: UserModel = Depends(validate_api_key)):
    return AgentsAPIView().delete_agent(agent_id, user.id)