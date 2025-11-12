
import os
import logging

from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.tools import Tool

from database.models.agent import AgentModel
from core.database.mongo import DatabaseHandler
from models import agent

logger = logging.getLogger(__name__)

load_dotenv()

MONGO_HISTORY_COLLECTION = os.getenv("MONGODB_HISTORY_COLLECTION")

class BaseAgent:
    def __init__(self):
        self.ollama_model_name = os.getenv("OLLAMA_MODEL")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL")
        self.openai_model_name = os.getenv("OPENAI_MODEL")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.agent = None
        self.database_handler = DatabaseHandler(MONGO_HISTORY_COLLECTION)
    
    def get_ollama_model(self):
        logger.info(f"Getting ollama model: {self.ollama_model_name}")
        return OpenAIChatModel(
            model_name=self.ollama_model_name,
            provider=OllamaProvider(base_url=self.ollama_base_url),
        )
    
    def get_openai_model(self):
        logger.info(f"Getting openai model: {self.openai_model_name}")
        return OpenAIChatModel(
            model_name=self.openai_model_name,
            provider=OpenAIProvider(api_key=self.openai_api_key),
        )
    
    def build_agent(self, agent_obj: AgentModel, tools: list[Tool], system_prompt: str):
        logger.info(f"Building agent with tools: {tools} and system prompt: {system_prompt}")

        if agent_obj.provider == "openai":
            model = self.get_openai_model()
        else:
            model = self.get_ollama_model()

        self.agent = Agent(
            model, 
            tools=tools,
            system_prompt=system_prompt,
        )
        return self.agent
    
    def execute(self, user_input: str, is_final_response: bool = False):
        try:
            logger.info(f"Executing agent: {self.agent}")

            if self.agent_obj:
                logger.info("Loading agent history")
                agent_history = self.database_handler.load_history_json(self.agent_obj.user_id, self.agent_obj.id)
                logger.info(f"Retrieved {len(agent_history)} messages from history")
            else:
                logger.info("No history loaded")
                agent_history = []

            response = self.agent.run_sync(user_input, message_history=agent_history)
            agent_response = response.output

            if is_final_response:
                agent_id = self.agent_obj.id
                user_id = self.agent_obj.user_id
                self.database_handler.insert_history(user_input, agent_response, user_id, agent_id)

            return agent_response
        except Exception as e:
            logger.error(f"Error to execute agent: {e}")
            raise e
    