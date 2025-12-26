import os
import logging

from pathlib import Path
from typing import Optional
from markdown_pdf import MarkdownPdf, Section

from pydantic_ai.tools import Tool
from pydantic_ai.common_tools.tavily import tavily_search_tool

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
        Search the web for information.
        """
        logger.info("Using Tavily Search Tool")
        return tavily_search_tool(self.tavily_search_api_key)

    # ================================
    # Document Handling Tools
    # ================================

    def create_text_document_tool(self):
        """
        Create a text document with LLM-generated content.
        """
        @Tool
        def create_text_document(
            filename: str,
            content: str,
            directory: Optional[str] = None
        ) -> str:
            """
            Create a PLAIN TEXT (.txt) file with the specified content.
            
            ⚠️ ONLY use this tool for:
            - Plain text files, notes, or simple documents
            - When user explicitly asks for a .txt or text file
            - When the query contains "[FORMAT: TEXT]"
            
            ❌ DO NOT use for PDFs - use create_pdf_document instead
            
            Args:
                filename: Name of the file to create (without extension, .txt will be added automatically)
                content: The plain text content to write to the file
                directory: Optional subdirectory within the output folder
            
            Returns:
                Success message with file path
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
        """
        Create a pdf document with LLM-generated content.
        """
        @Tool
        def create_pdf_document(
            filename: str,
            content: str,
            directory: Optional[str] = None
        ) -> str:
            """
            Create a PDF (.pdf) file from markdown content.
            
            ✅ USE THIS TOOL for:
            - PDF files
            - When user asks for "pdf" or "PDF"
            - When the query contains "[FORMAT: PDF]"
            - Formatted documents, reports, or professional content
            
            ❌ DO NOT use for plain text files - use create_text_document instead
            
            Args:
                filename: Name of the file to create (without extension, .pdf will be added automatically)
                content: The markdown content to write to the file.
                directory: Optional subdirectory within the output folder
            
            Returns:
                Success message with file path
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