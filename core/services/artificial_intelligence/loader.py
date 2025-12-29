import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader


class FileLoader:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def _file_loaders(self):
        return {
            ".pdf": PyPDFLoader,
            ".docx": Docx2txtLoader,
            ".txt": TextLoader
        }
    
    def _get_loader(self):
        _, extension = os.path.splitext(self.file_path)
        available_loaders = self._file_loaders()
        loader = available_loaders.get(extension)

        if not loader:
            return None

        self.loader = loader(self.file_path)
        return loader(self.file_path)

    def _load_and_split_file(self):
        loader = self._get_loader()
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        documents_splitted = text_splitter.split_documents(documents)

        return documents_splitted