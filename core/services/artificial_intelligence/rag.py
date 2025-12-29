import os
import logging

from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.Logger(__name__)

load_dotenv()

class RAG:
    def __init__(self):
        self.model_name = os.getenv("EMBEDDING_MODEL")
        self.model = HuggingFaceEmbeddings(model_name=self.model_name)
    
    def embedding_sentence(self, sentence) -> list:
        logging.info(f"Embedding sentence: {sentence[:50]}...")

        try:
            return self.model.embed_query(sentence)
        except Exception as e:
            logger.error(f"Error to embed sentence: {e}")
            raise e

    def embedding_documents(self, documents) -> list:
        logging.info(f"Embedding documents: {len(documents)} documents")

        try:
            return self.model.embed_documents(documents)
        except Exception as e:
            logger.error(f"Error to embed documents: {e}")
            raise e
    
    def retrieve_documents_by_similarity(self, index_name: str, query: str, top_k: int) -> list:
        from core.database.opensearch import OpenSearchHandler
        logging.info("Retrieving documents")
        opensearch_handler = OpenSearchHandler(index_name=index_name)

        try:
            documents = opensearch_handler.retrieve_documents(query=query, top_k=top_k)
            return documents
        except Exception as e:
            logger.error(f"Error to embed documents: {e}")
            raise e
    
    def load_file_and_embed(self, index_name: str, file_path: str):
        from core.database.opensearch import OpenSearchHandler
        from core.services.artificial_intelligence import FileLoader

        try:
            file_loader = FileLoader(file_path)
            vector_database_handler = OpenSearchHandler(index_name)

            documents = file_loader._load_and_split_file()

            status = vector_database_handler.insert_documents(documents)

            if status["Status"] == "Failed":
                raise HTTPException(status_code=404, detail=status["Message"])
            
            return True

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error to upload file: {e}")