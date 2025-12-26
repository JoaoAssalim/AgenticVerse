import logging

from pydantic_ai import RunContext

from database.models.agent import AgentModel
from core.agents.base_agent import BaseAgent
from core.agents.base_agent import AgentDeps
from core.agents.agent_tools.web_search_agent import WebSearchAgent
from core.agents.agent_tools.document_handler_agent import DocumentHandlerAgent

logger = logging.Logger(__name__)

class OrchestratorAgent(BaseAgent):
    def __init__(self, agent_obj: AgentModel):
        super().__init__()
        self.agent_obj = agent_obj
        self.available_tools = {
            "web_search": self.web_search_tool,
            "handle_documents": self.document_handler_tool
        }

        self.search_worker_agent = WebSearchAgent(self.agent_obj)
        self.document_handler_agent = DocumentHandlerAgent(self.agent_obj)

        self.agent = self.build_agent(
            self.agent_obj,
            tools=[
                self.available_tools.get(tool) for tool in self.agent_obj.tools
            ],
            system_prompt=self._generate_system_prompt()
        )

    def _generate_system_prompt(self):
        return f"""You are an AI Assistant with web search and document creation capabilities.

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

        USER_PROMPT: {self.agent_obj.system_prompt}"""

    def web_search_tool(self, ctx: RunContext[AgentDeps], query: str):
        logger.info("Calling WebSearch Tool")
        return self.search_worker_agent.execute(query, is_tool_agent=True, deps=ctx.deps)
    
    def document_handler_tool(self, ctx: RunContext[AgentDeps], query: str):
        logger.info("Calling Document Handler Tool")
        return self.document_handler_agent.execute(query, is_tool_agent=True, deps=ctx.deps)
