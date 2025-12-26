import os
import ssl
import certifi

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()


class SlackHandler:
    def __init__(self):
        # Create SSL context using certifi's CA bundle
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.client = WebClient(
            token=os.getenv("SLACK_BOT_USER_OAUTH_TOKEN"),
            ssl=ssl_context
        )

    def send_message(self, channel_id: str, message: str):
        try:
            response = self.client.chat_postMessage(
                channel=channel_id,
                text=message,
            )
            return response
        except SlackApiError as e:
            assert e.response["error"]

    def get_user_by_id(self, user_id: str):
        try:
            response = self.client.users_info(
                include_locale=False,
                user=user_id,
            )

            return response
        except SlackApiError as e:
            assert e.response["error"]