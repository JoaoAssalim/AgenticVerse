import os

from celery import Celery
from dotenv import load_dotenv
from pydantic_ai import RunContext

from core.api import AgentsAPIView
from core.agents.base_agent import AgentDeps
from core.agents.agent_orchestrator import OrchestratorAgent

load_dotenv()

celery = Celery(
    "worker",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)

@celery.task
def execute_agent_task(message, user_id, agent_id, ctx: RunContext[AgentDeps]):
    try:
        agent = AgentsAPIView().get_agent(agent_id, user_id)

        agent = OrchestratorAgent(agent)
        response = agent.execute(message, is_tool_agent=False, deps=ctx)
        return {"message": response}
    except Exception as e:
        return {"error": str(e)}