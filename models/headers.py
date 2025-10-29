from pydantic import BaseModel

class CommonHeaders(BaseModel):
    agent_id: str