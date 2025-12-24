import os
import logging

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

from core.database.opensearch import OpenSearchHandler

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
        logging.info("Retrieving documents")
        opensearch_handler = OpenSearchHandler(index_name=index_name)

        try:
            documents = opensearch_handler.retrieve_documents(query=query, top_k=top_k)
            return documents
        except Exception as e:
            logger.error(f"Error to embed documents: {e}")
            raise e