import os
import asyncio
import logging

from typing import Annotated
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, Header, WebSocket, WebSocketDisconnect

from core.api import AgentsAPIView
from database.models.users import UserModel
from core.agents.base_agent import AgentDeps
from core.websocket import ConnectionManager
from database.models.agent import AgentModel
from core.database.mongo import DatabaseHandler
from core.auth import validate_api_key, validate_api_key_websocket
from models import AgentRequest, AgentBaseModel, AgentUpdateModel, CommonHeaders

logger = logging.getLogger(__name__)

MONGO_HISTORY_COLLECTION = os.getenv("MONGODB_HISTORY_COLLECTION")

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    responses={404: {"description": "Not found"}},
)

manager = ConnectionManager()

@router.websocket("/ws/execute")
async def websocket_invoke_agent(websocket: WebSocket):
    
    logger.info("Starting Websocket...")

    headers = websocket.headers
    user = await validate_api_key_websocket(headers.get("x-api-key", None))

    logger.info(f"User {user.name} validated to WebSocket")

    from celery_worker import execute_agent_task

    await manager.connect(websocket)
    try:
        data = await websocket.receive_json()
        task = execute_agent_task.delay(data.get("message"), user.id, data.get("agent_id"))

        logger.info(f"Task created with id: {task.id}")

        await manager.send_personal_message({
            "task_id": task.id,
            "status": "started"
        }, websocket)

        while True:
            task_result = get_invoke_result(task.id)

            await manager.send_personal_message(task_result, websocket)

            if task_result.get("status") in ["completed", "failed"]:
                logger.info(f"Task finished with status: {task_result.get("status")}")
                break

            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        logger.error("Websocket disconnected")
        pass
    except Exception as e:
        logger.error(f"Error to execute websocket: {e}")
        await manager.send_personal_message({
            "status": "error",
            "message": str(e)
        }, websocket)
    finally:
        try:
            await manager.disconnect(websocket)
        except Exception:
            pass

@router.get("/get-async-agent-result/{task_id}")
def get_invoke_result(task_id: str, user: UserModel = Depends(validate_api_key)):
    logger.info(f"Getting task status with id: {task_id} for user: {user.name}")

    try:
        task_result = AsyncResult(task_id)
        if task_result.ready():
            return {"task_id": task_id, "status": "completed", "result": task_result.result}
        elif task_result.failed():
            return {"task_id": task_id, "status": "failed", "result": {"message": "Agent cannot process your request."}}
        else:
            return {"task_id": task_id, "status": "in progress", "result": {"message": "Agent is processing your request..."}}
    except Exception as e:
        logger.error(f"Error to get task result: {e}")
        raise e

@router.post("/execute/async")
def invoke_agent_async(request: AgentRequest, header: Annotated[CommonHeaders, Header()], user: UserModel = Depends(validate_api_key)):
    logger.info(f"Executing agent ({header.agent_id}) asynchronously")
    from celery_worker import execute_agent_task

    try:
        task = execute_agent_task.delay(request.message, user.id, header.agent_id)
        return {"task_id": task.id}
    except Exception as e:
        logger.error(f"Error to execute agent asynchronously: {e}")
        raise e

@router.post("/execute/sync")
def invoke_agent_sync(request: AgentRequest, header: Annotated[CommonHeaders, Header()], user: UserModel = Depends(validate_api_key)):
    logger.info(f"Executing agent ({header.agent_id}) synchronously")
    from core.agents.agent_orchestrator import OrchestratorAgent

    try:
        agent = AgentsAPIView().get_agent(header.agent_id, user.id)

        deps = AgentDeps(
            db=DatabaseHandler(MONGO_HISTORY_COLLECTION),
            user_id=str(user.id),
            agent_id=str(header.agent_id)
        )

        agent = OrchestratorAgent(agent)
        response = agent.execute(request.message, is_tool_agent=False, deps=deps)
        return {"message": response}
    except Exception as e:
        logger.error(f"Error to execute agent synchronously: {e}")
        raise e

@router.post("/create")
def create_agent(agent: AgentBaseModel, user: UserModel = Depends(validate_api_key)):
    logger.info("Creating agent")
    try:
        agent_model = agent.model_dump_json()
        logger.info(f"Agent data: {agent_model}")
        agent_model = AgentModel.model_validate_json(agent_model)
        return AgentsAPIView().create_agent(agent_model, user.id)
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise e

@router.patch("/update/{agent_id}")
def update_agent(agent_id: str, agent: AgentUpdateModel, user: UserModel = Depends(validate_api_key)):
    logger.info("Updating agent")
    try:
        agent_model = agent.model_dump_json(exclude_unset=True)
        logger.info(f"Agent data: {agent_model}")
        agent_model = AgentModel.model_validate_json(agent_model)
        return AgentsAPIView().update_agent(agent_id, agent_model, user.id)
    except Exception as e:
        logger.error(f"Error updating agent: {e}")
        raise e
    
@router.get("/get/{agent_id}")
def get_agent(agent_id: str, user: UserModel = Depends(validate_api_key)):
    logger.info(f"Getting agent with id: {agent_id}")
    try:
        return AgentsAPIView().get_agent(agent_id, user.id)
    except Exception as e:
        logger.error(f"Error getting agent ({agent_id}): {e}")
        raise e

@router.get("/get-all")
def get_all_agents(user: UserModel = Depends(validate_api_key)):
    logger.info("Getting all agents")
    try:
        return AgentsAPIView().get_all_agents(user.id)
    except Exception as e:
        logger.error(f"Error getting agents: {e}")
        raise e
    
@router.delete("/delete/{agent_id}")
def delete_agent(agent_id: str, user: UserModel = Depends(validate_api_key)):
    logger.info(f"Deleting agent with id: {agent_id}")
    try:
        return AgentsAPIView().delete_agent(agent_id, user.id)
    except Exception as e:
        logger.error(f"Error deleting agent: {e}")
        raise e
    