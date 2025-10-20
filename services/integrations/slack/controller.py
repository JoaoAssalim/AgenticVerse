import os
import json
import random

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from slack_sdk.signature import SignatureVerifier, Clock

from services.integrations.slack.handler import SlackHandler

load_dotenv()

class SlackController:
    def __init__(self):
        self.MESSAGE_TYPES = [
            "im"
        ]
        self.CHALLENGE_VARIFICATION = "url_verification"
        self.DEFAULT_MESSAGES = [
            "One moment, I'm processing your request...",
            "Please wait while I process your request...",
            "I'm working on it...",
            "I'm thinking...",
            "I'm processing your request...",
            "I'm processing your request...",
        ]
        self.ERROR_MESSAGE = "Sorry, I'm having trouble processing your request. Please try again later."
        self.slack_handler = SlackHandler()

    def is_challenge(self, data: dict) -> bool:
        return data.get("challenge") and data.get("type") == self.CHALLENGE_VARIFICATION
        
    def valid_signature(self, data: str, headers: dict) -> bool:
        signature_verifier = SignatureVerifier(
            signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
            clock=Clock()
        )

        return signature_verifier.is_valid_request(
            data,
            headers
        )

    async def handle_slack_event(self, request: dict):
        data = await request.body()
        json_data = json.loads(data)

        if self.is_challenge(json_data):
            return JSONResponse(content={"challenge": data.get("challenge")})

        if not self.valid_signature(data, request.headers):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        event_type = json_data.get("event", {}).get("channel_type", None)

        if event_type not in self.MESSAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid event type")

        try:
            message_info = json_data.get("event", {}).get("blocks", [])[0].get("elements", [])[0].get("elements", [])
            user_id = json_data.get("event", {}).get("user", None)
            text = message_info[-1].get("text", None)

            if not user_id or not text:
                raise HTTPException(status_code=400, detail="Invalid message info")

            slack_user_info = self.slack_handler.get_user_by_id(user_id)
            # Waiting message
            self.slack_handler.send_message(slack_user_info.get("user", {}).get("id", None), random.choice(self.DEFAULT_MESSAGES))

            return JSONResponse(content={"message": "OK"})
        
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail=f"Error: {e}")