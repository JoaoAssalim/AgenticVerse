import logging

from core.agents import BaseAgent
from database.schemas import AgentModel
from core.agents.agent_tools import AgentTools


logger = logging.Logger(__name__)

class OrchestratorAgent(BaseAgent):
    def __init__(self, agent_obj: AgentModel):
        super().__init__()
        self.agent_obj = agent_obj

        self.agent_tools = AgentTools()

        self.available_tools = {
            "web_search": [self.agent_tools.tavily_search()],
            "handle_documents": [self.agent_tools.create_pdf_document_tool(), self.agent_tools.create_text_document_tool()],
            "rag_context": [self.agent_tools.get_rag_context_tool(self.agent_obj.opensearch_index)]
        }

        agent_tools = self._build_agent_tools(self.agent_obj.tools)

        self.agent = self.build_agent(
            self.agent_obj,
            tools=agent_tools,
            system_prompt=self._generate_system_prompt(self.agent_obj.tools)
        )

    def _build_agent_tools(self, tools):
        agent_tools = []

        for tool in tools:
            agent_tool = self.available_tools.get(tool)

            if agent_tool:
                agent_tools.extend(agent_tool)
        
        return agent_tools


    def _build_rag_tool_prompt(self):
        return """
        get_rag_context
        - PRIMARY SOURCE: Mandatory tool for internal, technical, or private company data.
        - ACTION: You MUST call this tool first for any factual inquiry.
        - GROUNDING: Use the results to ground your entire response.
        """
    
    def _build_web_search_tool_prompt(self):
        return """
        tavily_search
        - SECONDARY SOURCE: Use only for external, real-time, or news-related queries.
        - FALLBACK: Only use this if the RAG context is empty or explicitly insufficient for the specific request.
        """
    
    def _build_document_handler_tool_prompt(self):
        return """
        document_handler_tool
        - Use ONLY when the user explicitly asks to create or save a document
        - Supported formats: PDF and TEXT
        """

    def _build_prompt_rules(self, tools):
        rules = []
        if tools:
            rules.append("\n" + "━" * 20 + "\n## CRITICAL DECISION HIERARCHY")

        if "rag_context" in tools:
            rules.append("1. ALWAYS check internal knowledge (rag_context) before attempting external searches.")
        
        if "web_search" in tools:
            rules.append("2. Use web_search ONLY if the RAG search returns no results or if the user asks for 'latest/today's' news.")
            
        if "handle_documents" in tools:
            rules.append("3. DOCUMENT CREATION: Only invoke document tools if the user explicitly says 'create a PDF' or 'save this as a file'.")

        rules.append("\n## PROHIBITED SEQUENCES")
        rules.append("- NEVER call web_search BEFORE calling rag_context.")
        rules.append("- NEVER create a document automatically without a direct user command.")
        
        return "\n".join(rules)

    def _generate_system_prompt(self, tools):

        partioned_prompts = {
            "web_search": self._build_web_search_tool_prompt(),
            "handle_documents": self._build_document_handler_tool_prompt(),
            "rag_context": self._build_rag_tool_prompt(),
        }

        base_prompt = """
        You are an Orchestrator Agent responsible for deciding which specialized agent or tool to use.

        Your primary goal is to route the user request to the MOST APPROPRIATE agent.

        ━━━━━━━━━━━━━━━━━━━━━━
        ## AVAILABLE CAPABILITIES

        """

        for e, tool in enumerate(tools):
            part_prompt = partioned_prompts.get(tool)

            if part_prompt:
                base_prompt += f"{e + 1}. {part_prompt}"

        base_prompt += self._build_prompt_rules(tools)

        base_prompt += f"""
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
    
        return base_prompt