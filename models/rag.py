from pydantic import BaseModel

class RetrieveContextRequest(BaseModel):
    query: str
    top_k: int