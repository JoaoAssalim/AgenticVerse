from services.agents.base_agent import BaseAgent
from services.agents.web_search_agent import WebSearchAgent
from services.agents.document_handler_agent import DocumentHandlerAgent

from pydantic_ai.tools import Tool

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__()

        self.agent = self.build_agent(
            tools=[
                self.web_search_tool(),
            ],
            system_prompt="""You are an AI Assistant that helps users with any task. You have access to web search for current information.

## CORE BEHAVIOR:
- Answer questions directly using your knowledge
- Use web_search when you need current/real-time information
- Be helpful, concise, and conversational

## WHEN TO USE WEB SEARCH:
- Current events, news, recent developments
- Real-time data (prices, weather, statistics)
- Latest releases, updates, or changes
- Information that might be outdated

## RESPONSE STYLE:
- Provide complete, helpful answers
- Use tools seamlessly when needed
- Be direct and avoid over-explaining your process
- Combine your knowledge with search results when beneficial

Help the user with whatever they need."""
        )

    def web_search_tool(self):
        search_agent = WebSearchAgent()

        @Tool
        def call_web_search_agent(query: str) -> str:
            """Delegate a search task to the WebSearchAgent"""
            return search_agent.execute(query)
        return call_web_search_agent