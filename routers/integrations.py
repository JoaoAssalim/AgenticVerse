from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse

from services.integrations.slack.controller import SlackController

router = APIRouter(
    prefix="/integrations",
    tags=["integrations"],
    responses={404: {"description": "Not found"}},
)

@router.post("/slack/listener") # After configure database, we will need to pass agent uuid and integrations uuid
async def slack_listener(request: Request):
    slack_controller = SlackController()
    return await slack_controller.handle_slack_event(request)
