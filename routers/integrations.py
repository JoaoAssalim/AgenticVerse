import os
import discord
import asyncio
import logging

from fastapi import Request
from fastapi import APIRouter
from dotenv import load_dotenv

from core.services.integrations.discord import DiscordController
from core.services.integrations.slack.controller import SlackController

load_dotenv()

logger = logging.Logger(__name__)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

router = APIRouter(
    prefix="/integrations",
    tags=["Integrations"],
    responses={404: {"description": "Not found"}},
)

@router.post("/slack/listener") # After configure database, we will need to pass agent uuid and integrations uuid
async def slack_listener(request: Request):
    slack_controller = SlackController()
    return await slack_controller.handle_slack_event(request)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    discord_controller = DiscordController(client=client, message=message)
    await discord_controller.handle_discord_event()
    
def discord_listener():
    asyncio.create_task(client.start(os.getenv("DISCORD_TOKEN")))