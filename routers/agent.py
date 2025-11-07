import asyncio

from fastapi import APIRouter, Depends, Header, WebSocket, WebSocketDisconnect
from typing import Annotated
from celery.result import AsyncResult

from core.api import AgentsAPIView
from core.auth import validate_api_key
from core.websocket import ConnectionManager
from database.models.users import UserModel
from database.models.agent import AgentModel
from models import AgentRequest, AgentBaseModel, AgentUpdateModel, CommonHeaders

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    responses={404: {"description": "Not found"}},
)

manager = ConnectionManager()

@router.websocket("/ws/get-agent-response/{user_id}")
async def websocket_invoke_agent(websocket: WebSocket, user_id: str):
    from celery_worker import execute_agent_task

    await manager.connect(websocket)
    try:
        data = await websocket.receive_json()
        task = execute_agent_task.delay(data.get("message"), user_id, data.get("agent_id"))

        while True:
            task_result = get_invoke_result(task.id)

            await manager.send_personal_message(task_result, websocket)

            if task_result.get("status") in ["completed", "failed"]:
                await manager.disconnect(websocket)
                break

            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        await manager.send_personal_message({
            "status": "error",
            "message": str(e)
        }, websocket)
        await manager.disconnect(websocket)

@router.get("/get-async-agent-result/{task_id}")
def get_invoke_result(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.ready():
        return {"task_id": task_id, "status": "completed", "result": task_result.result}
    elif task_result.failed():
        return {"task_id": task_id, "status": "failed"}
    else:
        return {"task_id": task_id, "status": "in progress"}

@router.post("/execute/async")
def invoke_agent_async(request: AgentRequest, header: Annotated[CommonHeaders, Header()], user: UserModel = Depends(validate_api_key)):
    from celery_worker import execute_agent_task

    try:
        task = execute_agent_task.delay(request.message, user.id, header.agent_id)
        return {"task_id": task.id}
    except Exception as e:
        raise e

@router.post("/execute/sync")
def invoke_agent_sync(request: AgentRequest, header: Annotated[CommonHeaders, Header()], user: UserModel = Depends(validate_api_key)):
    from services.agent_orchestrator import OrchestratorAgent

    try:
        agent = AgentsAPIView().get_agent(header.agent_id, user.id)

        agent = OrchestratorAgent(agent)
        response = agent.execute(request.message)
        return {"message": response}
    except Exception as e:
        raise e

@router.post("/create")
def create_agent(agent: AgentBaseModel, user: UserModel = Depends(validate_api_key)):
    try:
        agent_model = agent.model_dump_json()
        agent_model = AgentModel.model_validate_json(agent_model)
        return AgentsAPIView().create_agent(agent_model, user.id)
    except Exception as e:
        raise e

@router.patch("/update/{agent_id}")
def update_agent(agent_id: str, agent: AgentUpdateModel, user: UserModel = Depends(validate_api_key)):
    try:
        agent_model = agent.model_dump_json(exclude_unset=True)
        agent_model = AgentModel.model_validate_json(agent_model)
        return AgentsAPIView().update_agent(agent_id, agent_model, user.id)
    except Exception as e:
        raise e
    
@router.get("/get/{agent_id}")
def get_agent(agent_id: str, user: UserModel = Depends(validate_api_key)):
    try:
        return AgentsAPIView().get_agent(agent_id, user.id)
    except Exception as e:
        raise e

@router.get("/get-all")
def get_all_agents(user: UserModel = Depends(validate_api_key)):
    try:
        return AgentsAPIView().get_all_agents(user.id)
    except Exception as e:
        raise e
    
@router.delete("/delete/{agent_id}")
def delete_agent(agent_id: str, user: UserModel = Depends(validate_api_key)):
    try:
        return AgentsAPIView().delete_agent(agent_id, user.id)
    except Exception as e:
        raise e
    