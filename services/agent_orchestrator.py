import logging

from database.models.agent import AgentModel
from services.agents.base_agent import BaseAgent
from services.agents.web_search_agent import WebSearchAgent
from services.agents.document_handler_agent import DocumentHandlerAgent

from pydantic_ai.tools import Tool

logger = logging.Logger(__name__)

class OrchestratorAgent(BaseAgent):
    def __init__(self, agent_obj: AgentModel):
        super().__init__()
        self.agent_obj = agent_obj
        self.available_tools = {
            "web_search": self.web_search_tool(),
            "handle_documents": self.document_handler_tool()
        }

        self.agent = self.build_agent(
            self.agent_obj,
            tools=[
                self.available_tools.get(tool) for tool in self.agent_obj.tools
            ],
            system_prompt=f"""You are an AI Assistant with web search and document creation capabilities.

TOOLS:
- call_web_search_agent: Real-time info (news, prices, current events, recent updates)
- call_document_handler_agent: Create .txt or .pdf files

CRITICAL - DOCUMENT FORMAT:
When calling document_handler_agent, ALWAYS prepend query with:
- "[FORMAT: PDF]" for PDFs or structured/professional content
- "[FORMAT: TEXT]" for plain text files or simple notes

Examples:
- "create pdf report" → "[FORMAT: PDF] create report..."
- "save as text" → "[FORMAT: TEXT] save..."

BEHAVIOR:
- Answer directly from knowledge when possible
- Use web_search for current/real-time information
- Create documents only when user explicitly requests
- Chain tools when needed (search → document)
- Be concise and helpful

USER_PROMPT: {agent_obj.system_prompt}"""
        )

    def web_search_tool(self):
        logger.info("Calling WebSearch Tool")
        search_agent = WebSearchAgent(self.agent_obj)

        @Tool
        def call_web_search_agent(query: str) -> str:
            """Delegate a search task to the WebSearchAgent"""
            return search_agent.execute(query)
        return call_web_search_agent
    
    def document_handler_tool(self):
        logger.info("Calling Document Handler Tool")
        document_handler_agent = DocumentHandlerAgent(self.agent_obj)

        @Tool
        def call_document_handler_agent(query: str):
            """Delegate a text document task to the DocumentHandlerAgent"""
            return document_handler_agent.execute(query)
        return call_document_handler_agent
