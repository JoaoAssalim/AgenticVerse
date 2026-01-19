import os
import asyncio

from dotenv import load_dotenv

from fastapi.responses import JSONResponse

from core.agents import AgentDeps
from core.agents import OrchestratorAgent
from core.api.agents import AgentsAPIView
from core.database.mongo import DatabaseHandler
from core.services.integrations.discord import DiscordHandler

load_dotenv()

MONGO_HISTORY_COLLECTION = os.getenv("MONGODB_HISTORY_COLLECTION")

class DiscordController:
    def __init__(self, client, message):
        self.DISCORD_BOT_ID = "<@&1460661205461893133>"
        self.client = client
        self.message = message

        self.ERROR_MESSAGE = "Sorry, I'm having trouble processing your request. Please try again later."

        self.discord_handler = DiscordHandler(message=message)
        self.discord_agent_obj = AgentsAPIView().get_or_create("Discord Bot")
        self.discord_agent = OrchestratorAgent(self.discord_agent_obj)

        self.agent_deps = AgentDeps(
            db=DatabaseHandler(MONGO_HISTORY_COLLECTION),
            user_id=None,
            agent_id=str(self.discord_agent_obj.id)
        )

    async def handle_discord_event(self):
        if self.message.author == self.client.user:
            return

        message_content = self.message.content

        if self.DISCORD_BOT_ID in message_content:
            message_content = message_content.replace(self.DISCORD_BOT_ID, "")

            ai_response = await asyncio.to_thread(
                self.discord_agent.execute,
                user_input=message_content,
                deps=self.agent_deps,
                is_tool_agent=False,
            )

            await self.discord_handler.send_message(ai_response)
        
        return JSONResponse(content={"message": "OK"})
    