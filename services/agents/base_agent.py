
import os
import logging

from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.tools import Tool

logger = logging.getLogger(__name__)

load_dotenv()

class BaseAgent:
    def __init__(self):
        self.model_name = os.getenv("OLLAMA_MODEL")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL")
        self.agent = None
    
    def get_ollama_model(self):
        logger.info(f"Getting ollama model: {self.model_name}")
        return OpenAIChatModel(
            model_name=self.model_name,
            provider=OllamaProvider(base_url=self.ollama_base_url),
        )
    
    def build_agent(self, tools: list[Tool], system_prompt: str):
        logger.info(f"Building agent with tools: {tools} and system prompt: {system_prompt}")
        model = self.get_ollama_model()
        self.agent = Agent(
            model, 
            tools=tools,
            system_prompt=system_prompt,
        )
        return self.agent
    
    def execute(self, prompt: str):
        logger.info(f"Executing agent: {self.agent}")
        response = self.agent.run_sync(prompt)
        return response.output
    