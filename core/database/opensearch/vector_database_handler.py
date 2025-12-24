import os
import logging

from dotenv import load_dotenv
from opensearchpy import OpenSearch
from langchain_community.vectorstores import OpenSearchVectorSearch

from services.artificial_intelligence import RAG

logger = logging.Logger(__name__)

load_dotenv()

class OpenSearchHandler:
    def __init__(self, index_name: str):
        self.index_name = index_name

        host = os.getenv("OPENSEARCH_HOST")
        port = os.getenv("OPENSEARCH_PORT")
        auth = ('admin', 'admin')

        self.client = OpenSearch(
            hosts = [{'host': host, 'port': port}],
            http_compress = True,
            http_auth = auth,
            use_ssl = False,
            verify_certs = False,
        )

        self.embedding_size = os.getenv("EMBEDDING_SIZE")
        self.rag_handler = RAG()

        self.handler = OpenSearchVectorSearch(
            opensearch_url=os.getenv("OPENSEARCH_URL"),
            index_name=self.index_name,
            embedding_function=self.rag_handler.model
        )

    def index_exists(self, index_name):
        return self.client.indices.exists(index=index_name)

    def create_index(self):
        logger.info(f"Creating Index: {self.index_name}")

        if not self.index_exists(self.index_name):
            try:
                index_body = {
                    'settings': {
                        'index': {
                            'number_of_shards': 1,
                            'number_of_replicas': 1,
                            'knn': True
                        }
                    },
                    "mappings": {
                        "properties": {
                            "vector_field": {
                                "type": "knn_vector",
                                "dimension": self.embedding_size,
                            }
                        }
                    }
                }

                self.client.indices.create(index=self.index_name, body=index_body)
            except Exception as e:
                logger.error(f"Error to create index: {e}")
                raise e

        return self.index_name
    
    def delete_index(self):
        logger.info(f"Deleting Index: {self.index_name}")

        if self.index_exists(self.index_name):
            try:
                self.handler.delete_index(index_name=self.index_name)
                return True
            except Exception as e:
                logger.error(f"Error to delete index: {e}")
                raise e

        return False

    def insert_documents(self, documents: list):
        logger.info(f"Inserting documents into index: {self.index_name}")

        if self.index_exists(self.index_name):
            try:
                self.handler.add_documents(documents)
                return {"Status": "Success", "Message": "Documents on database"}
            except Exception as e:
                logger.error(f"Error to delete index: {e}")
                raise e

        return {"Status": "Failed", "Message": "Agent not found"}
    
    def retrieve_documents(self, query:str, top_k: int):
        logger.info(f"Retrieving documents: {self.index_name}")

        if self.index_exists(self.index_name):
            try:
                documents = self.handler.similarity_search(query=query, k=top_k)
                return documents
            except Exception as e:
                logger.error(f"Error to delete index: {e}")
                raise e

        return []