import logging

from pydantic_ai import RunContext

from database.schemas import AgentModel
from core.agents import BaseAgent, AgentDeps
from core.agents.agent_tools import WebSearchAgent, DocumentHandlerAgent, RAGAgent


logger = logging.Logger(__name__)

class OrchestratorAgent(BaseAgent):
    def __init__(self, agent_obj: AgentModel):
        super().__init__()
        self.agent_obj = agent_obj
        self.available_tools = {
            "web_search": self.web_search_tool,
            "handle_documents": self.document_handler_tool,
            "rag_context": self.rag_context_tool
        }

        agent_tools = [self.available_tools.get(tool) for tool in self.agent_obj.tools]

        self.agent = self.build_agent(
            self.agent_obj,
            tools=agent_tools,
            system_prompt=self._generate_system_prompt()
        )

    def _generate_system_prompt(self):
        return f"""
        You are an Orchestrator Agent responsible for deciding which specialized agent or tool to use.

        Your primary goal is to route the user request to the MOST APPROPRIATE agent.

        ━━━━━━━━━━━━━━━━━━━━━━
        ## AVAILABLE CAPABILITIES

        1. rag_context_tool
        - Retrieves knowledge from the internal knowledge base (RAG)
        - Use this FIRST for factual, technical, or domain-specific questions
        - Preferred source for internal documentation and indexed content

        2. web_search_tool
        - Use ONLY for real-time, current, or external information
        - Examples: news, live prices, recent events, latest updates

        3. document_handler_tool
        - Use ONLY when the user explicitly asks to create or save a document
        - Supported formats: PDF and TEXT

        ━━━━━━━━━━━━━━━━━━━━━━
        ## DECISION RULES (CRITICAL)

        1. If the question can be answered using internal knowledge → USE rag_context_tool FIRST
        2. Only use web search if:
        - The user explicitly asks for recent/current information, OR
        - RAG does not contain enough information
        3. NEVER use web search if RAG is sufficient
        4. ONLY create documents if the user explicitly requests it
        5. NEVER create documents implicitly

        ━━━━━━━━━━━━━━━━━━━━━━
        ## TOOL CHAINING RULES

        - Allowed:
        rag_context_tool → document_handler_tool
        rag_context_tool → web_search_tool (only if insufficient context)

        - NOT allowed:
        web_search_tool → rag_context_tool
        document_handler_tool without explicit user request

        ━━━━━━━━━━━━━━━━━━━━━━
        ## RESPONSE STYLE

        - Be concise and direct
        - Do not expose internal reasoning
        - Do not fabricate information
        - Clearly signal when information is unavailable

        ━━━━━━━━━━━━━━━━━━━━━━
        USER PROMPT CONTEXT:
        {self.agent_obj.system_prompt}
        """

    def web_search_tool(self, ctx: RunContext[AgentDeps], query: str):
        logger.info("Calling WebSearch Tool")
        search_worker_agent = WebSearchAgent(self.agent_obj)
        return search_worker_agent.execute(query, is_tool_agent=True, deps=ctx.deps)
    
    def document_handler_tool(self, ctx: RunContext[AgentDeps], query: str):
        logger.info("Calling Document Handler Tool")
        document_handler_agent = DocumentHandlerAgent(self.agent_obj)
        return document_handler_agent.execute(query, is_tool_agent=True, deps=ctx.deps)

    def rag_context_tool(self, ctx: RunContext[AgentDeps], query: str):
        logger.info("Calling RAG Context Handler Tool")
        rag_agent = RAGAgent(self.agent_obj)
        return rag_agent.execute(query, is_tool_agent=True, deps=ctx.deps)