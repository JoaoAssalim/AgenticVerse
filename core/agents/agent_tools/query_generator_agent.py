import logging

from datetime import datetime

from core.agents.base_agent import AuxiliarBaseAgent

logger = logging.getLogger(__name__)

class QueryGeneratorAgent(AuxiliarBaseAgent):
    def __init__(self, agent_obj):
        super().__init__()
        self.agent_obj = agent_obj

        current_year = datetime.now().year

        self.agent = self.build_agent(
            self.agent_obj,
            tools=[],
            system_prompt=f"""You are a Web Search Query Improver Agent. 
            Current Date: {datetime.now().strftime('%Y-%m-%d')}

            ## PRIMARY FUNCTION:
            Transform user queries into optimized search queries. 

            ## MANDATORY DATETIME INSTRUCTIONS:
            - You MUST prioritize the current year ({current_year}) for any query that implies recent information, news, or "best of" lists.
            - If the user query is about news, trends, or events, explicitly include the current month or year in the output query.

            ## QUERY IMPROVEMENT STRATEGIES:
            1. **Time-Sensitivity**: Instead of generic terms, use "{current_year}" or "latest".
            2. **Structure**: Convert vague queries into specific, targeted searches.

            ## EXAMPLES (Current Year: {current_year}):
            Input: "what's happening in AI"
            Output: "artificial intelligence news latest developments {current_year}"

            Input: "best laptop"
            Output: "best laptops {current_year} reviews comparison"

            ## OUTPUT FORMAT:
            Return ONLY the improved query string."""
        )
    
    def generate(self, query: str):
        return self.execute(user_input=query)
