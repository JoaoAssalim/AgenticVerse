import os
import logging

from fastapi import APIRouter, Depends, UploadFile

from core.auth import validate_api_key
from core.api.agents import AgentsAPIView
from database.models.users import UserModel
from core.services.artificial_intelligence import RAG
from core.services.artificial_intelligence.helpers import validate_file, save_file_locally

logger = logging.Logger(__name__)

router = APIRouter(
    prefix="/rag",
    tags=["rag"],
    responses={404: {"description": "Not found"}},
)

@router.post("/upload-file/{agent_id}")
def update_user(agent_id: str, file: UploadFile, user: UserModel = Depends(validate_api_key)):
    logger.info(f"Uploading file to agent: {agent_id}")
    rag = RAG()

    try:
        agent = AgentsAPIView().get_agent(agent_id=agent_id, user_id=user.id)

        file_path = save_file_locally(file)
        validate_file(file_path, file.size)

        rag.load_file_and_embed(index_name=agent.opensearch_index, file_path=file_path)

        os.remove(file_path)
        
        return {"Status": "Sucess", "Message": "File was saved on vector database"}

    except Exception as e:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass

        raise e
