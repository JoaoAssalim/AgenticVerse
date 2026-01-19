import os
import logging

from fastapi import APIRouter, Depends, UploadFile, HTTPException

from core.auth import validate_api_key
from database.schemas import UserModel
from core.api.agents import AgentsAPIView
from models.rag import RetrieveContextRequest
from core.services.artificial_intelligence import RAG
from core.database.opensearch import OpenSearchHandler
from core.utils.permissions import handle_user_permission
from core.services.artificial_intelligence.helpers import validate_file, save_file_locally


logger = logging.Logger(__name__)

agent_api = AgentsAPIView()

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
    responses={404: {"description": "Not found"}},
)

@router.post("/upload-file/{agent_id}")
def upload_file_to_vector_database(agent_id: str, file: UploadFile, user: UserModel = Depends(validate_api_key)):
    logger.info(f"Uploading file to agent: {agent_id}")

    try:
        handle_user_permission(user.group, ["user", "manager", "admin"])

        rag = RAG()
        agent = agent_api.get(agent_id=agent_id, user_id=user.id)

        file_path = save_file_locally(file)
        validate_file(file_path, file.size)

        rag.load_file_and_embed(index_name=agent.opensearch_index, file_path=file_path)

        os.remove(file_path)
        
        return {"Status": "Sucess", "Message": "File was saved on vector database"}
    except HTTPException as e:
        logger.error(f"Error to upload the file to agent: {agent_id}")
        raise e
    except Exception as e:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass

        raise e

@router.post("/retrieve-context/{agent_id}")
def retrieve_context_from_vector_database(agent_id: str, context: RetrieveContextRequest, user: UserModel = Depends(validate_api_key)):
    logger.info(f"Retrieving context from agent: {agent_id}")

    try:
        handle_user_permission(user.group, ["user", "manager", "admin"])

        rag = RAG()
        agent = agent_api.get(agent_id=agent_id, user_id=user.id)

        query, top_k = context.query, context.top_k
        content = rag.retrieve_documents_by_similarity(index_name=agent.opensearch_index, query=query, top_k=top_k)
        
        return content
    except HTTPException as e:
        logger.error(f"Error to retrieve the context to agent: {agent_id}")
        raise e
    except Exception as e:
        raise e

@router.delete("/clean-index/{agent_id}")
def clean_documents_from_index(agent_id: str, user: UserModel = Depends(validate_api_key)):
    logger.info(f"Deleting documents from index: {agent_id}")

    try:
        handle_user_permission(user.group, ["user", "manager", "admin"])
        
        agent = agent_api.get(agent_id=agent_id, user_id=user.id)
        opensearch_handler = OpenSearchHandler(index_name=agent.opensearch_index)

        opensearch_handler.clean_index()
        
        return {"Status": "Sucess", "Message": "Deleted all documents from agent"}
    
    except HTTPException as e:
        logger.error(f"Error to clean the index to agent: {agent_id}")
        raise e
    except Exception as e:
        raise e

