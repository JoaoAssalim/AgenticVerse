import os

from dotenv import load_dotenv
from celery import Celery

from core.api import AgentsAPIView
from services.agent_orchestrator import OrchestratorAgent

load_dotenv()

celery = Celery(
    "worker",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)

@celery.task
def execute_agent_task(message, user_id, agent_id):
    try:
        agent = AgentsAPIView().get_agent(agent_id, user_id)

        agent = OrchestratorAgent(agent)
        response = agent.execute(message)
        return {"message": response}
    except Exception as e:
        return {"error": str(e)}