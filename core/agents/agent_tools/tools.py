import os
import logging

from pathlib import Path
from typing import Optional
from markdown_pdf import MarkdownPdf, Section

from pydantic_ai.tools import Tool
from pydantic_ai.common_tools.tavily import tavily_search_tool

from core.services.artificial_intelligence import RAG

logger = logging.Logger(__name__)

class AgentTools:
    def __init__(self):
        self.tavily_search_api_key = os.getenv("TAVILY_API_KEY")
        self.output_dir = Path(os.getenv("OUTPUT_FILE_PATH"))
        self.output_dir.mkdir(exist_ok=True)

    
    # ================================
    # Web Search Tools
    # ================================
    
    def tavily_search(self):
        """
        SEARCH THE EXTERNAL INTERNET (SECONDARY SOURCE).
        
        ✅ USE ONLY IF:
        1. The RAG context did not provide enough information.
        2. The user is asking about current events, today's news, or real-time data (stock prices, weather).
        3. Information is specifically requested from the 'web' or 'internet'.

        ❌ DO NOT USE:
        - For internal company data.
        - If the RAG context already provides a sufficient answer.
        """
        logger.info("Using Tavily Search Tool")
        return tavily_search_tool(self.tavily_search_api_key)

    # ================================
    # Document Handling Tools
    # ================================

    def create_text_document_tool(self):
        @Tool
        def create_text_document(
            filename: str,
            content: str,
            directory: Optional[str] = None
        ) -> str:
            """
            WRITE A PLAIN TEXT (.txt) FILE TO STORAGE.

            ⚠️ MANDATORY TRIGGER: Use this tool ONLY when the user explicitly asks to "save", "export", 
            "create a file", or "write to a txt". 

            ✅ USE THIS TOOL FOR:
            - Saving raw notes, logs, or unformatted snippets.
            - Creating simple .txt files as requested by the user.
            - When the user specifically mentions "Text format" or ".txt".

            ❌ DO NOT USE FOR:
            - Generating a response in the chat (just reply normally for that).
            - Professional reports, tables, or formatted documents (USE create_pdf_document INSTEAD).
            - Storing data if the user didn't explicitly ask for a FILE.

            Args:
                filename: The name of the file. If no extension is provided, .txt will be appended.
                content: The literal string content to be written inside the file.
                directory: Optional sub-folder name to organize the file.

            Returns:
                A confirmation message with the absolute path of the created file.
            """
            logger.info("Using Text Document Handling Tool")
            try:
                # Validate content
                if not content or content.strip() == "":
                    return "Error: Content cannot be empty. Please provide actual text content to write to the file."
                
                # Determine the output path
                if directory:
                    output_path = self.output_dir / directory
                    output_path.mkdir(exist_ok=True)
                else:
                    output_path = self.output_dir
                
                # Ensure filename has .txt extension
                if not filename.endswith('.txt'):
                    filename += '.txt'
                
                file_path = output_path / filename
                
                # Write content to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return f"Successfully created text file: {file_path.absolute()}\nFile size: {len(content)} characters"
                
            except Exception as e:
                logger.error(f"Error to use text document tool: {e}")
                return f"Error creating text file: {str(e)}"
        
        return create_text_document

    def create_pdf_document_tool(self):
        @Tool
        def create_pdf_document(
            filename: str,
            content: str,
            directory: Optional[str] = None
        ) -> str:
            """
            EXPORT CONTENT TO PDF FILE.
            
            ⚠️ TRIGGER: ONLY use this tool if the user explicitly uses words like 'export', 'save as pdf', 
            'generate a report file', or 'create a document'. 
            
            ✅ USE FOR:
            - Formal reports, resumes, and multi-page formatted documents.
            - When visual structure and professional layout are required.
            
            ❌ PROHIBITED:
            - DO NOT call this tool unless the user specifically asked for a FILE to be generated.
            - DO NOT use for plain notes or simple lists (use create_text_document for those).
            """
            logger.info("Using PDF Document Handling Tool")
            try:
                # Validate content
                if not content or content.strip() == "":
                    return "Error: Content cannot be empty. Please provide actual markdown content to write to the file."
                
                # Determine the output path
                if directory:
                    output_path = self.output_dir / directory
                    output_path.mkdir(exist_ok=True)
                else:
                    output_path = self.output_dir
                
                # Ensure filename has .pdf extension
                if not filename.endswith('.pdf'):
                    filename += '.pdf'
                
                file_path = output_path / filename
                
                pdf = MarkdownPdf(toc_level=2)
                pdf.add_section(Section(content))
                pdf.save(file_path)
                
                return f"Successfully created pdf file: {file_path.absolute()}\nFile size: {len(content)} characters"
                
            except Exception as e:
                logger.error(f"Error to use text document tool: {e}")
                return f"Error creating pdf file: {str(e)}"
        
        return create_pdf_document
    
    # ================================
    # RAG Tools
    # ================================
    
    def get_rag_context_tool(self, index_name: str) -> list:
        @Tool
        def get_rag_context(query: str, top_k: int) -> list:
            """
            ACCESS INTERNAL KNOWLEDGE BASE (MANDATORY FIRST STEP).
            
            Use this tool ALWAYS as your first action for any factual, technical, or company-specific query.
            This tool performs a semantic search against our private database to provide verified context.

            ✅ USE FOR:
            - Verifying facts before answering.
            - Finding technical documentation, policies, or historical data.
            - Any query where the user asks about 'internal' or 'saved' info.

            ❌ DO NOT USE FOR:
            - Real-time news or external events (use tavily_search for that).
            - Creating files or formatting text.

            If this tool returns "No relevant context found", only then should you consider external tools.
            """
            logger.info(
                "Using RAG retrieval tool | index=%s | top_k=%s",
                index_name,
                top_k
            )
            try:
                rag = RAG()
                documents = rag.retrieve_documents_by_similarity(index_name=index_name, query=query, top_k=top_k)
                
                return documents
                
            except Exception as e:
                logger.error(f"Error to use RAG tool: {e}")
                return []
        
        return get_rag_context