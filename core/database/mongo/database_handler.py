import os
import uuid
import logging

from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    TextPart,
    UserPromptPart,
)

load_dotenv()

DATABASE_URL_CONNECTION = os.getenv("MONGODB_STRING_CONNECTION")
DATABASE_NAME = os.getenv("MONGODB_DATABASE_NAME")

logger = logging.getLogger(__name__)

class DatabaseHandler:
    def __init__(self, collection):
        logger.info(f"Starting Mongo Database for collection {collection}")
        self.collection = collection
        self.client = MongoClient(
            DATABASE_URL_CONNECTION,
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            maxPoolSize=10,
            retryWrites=True
        )
        self.database = self.client[DATABASE_NAME]
        self.collection_obj = self.database[self.collection]

    def insert_history(self, input: str, output: str, user_id: str, agent_id: str):
        logger.info(f"Inserting history for agent {agent_id}")
        try:
            self.collection_obj.insert_one({
                "runId": str(uuid.uuid4()),
                "agent_id": str(agent_id),
                "user_id": str(user_id),
                "input": input, 
                "output": output
            })
        except Exception as e:
            logger.error(f"Error to insert history do agent: {e}")
            raise e
     
    def load_history_json(self, user_id: str, agent_id: str):
        logger.info(f"Getting history for agent {agent_id}")
        try:
            history = self.collection_obj.find({
                "agent_id": str(agent_id),
                "user_id": str(user_id)
            })

            loaded_messages = []

            for message in history:
                
                # User input
                loaded_messages.append(
                    ModelRequest(parts=[UserPromptPart(content=message.get("input"))]),
                )

                #Ai response
                loaded_messages.append(
                    ModelResponse(parts=[TextPart(content=message.get("output"))]),
                )

            return loaded_messages

        except Exception as e:
            logger.error(f"Error to insert history do agent: {e}")
            raise e