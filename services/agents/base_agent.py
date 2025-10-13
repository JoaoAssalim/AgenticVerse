
import os
import logging

from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.tools import Tool

logger = logging.getLogger(__name__)

load_dotenv()

class BaseAgent:
    def __init__(self):
        self.ollama_model_name = os.getenv("OLLAMA_MODEL")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL")
        self.openai_model_name = os.getenv("OPENAI_MODEL")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.agent = None
        self.params = {}
    
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
    
    def build_agent(self, tools: list[Tool], system_prompt: str):
        logger.info(f"Building agent with tools: {tools} and system prompt: {system_prompt}")

        if self.params.get("provider") == "openai":
            model = self.get_openai_model()
        else:
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
    