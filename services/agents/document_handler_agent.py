from services.agents.base_agent import BaseAgent
from services.tools import AgentTools

class DocumentHandlerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.agent_tools = AgentTools()
        self.agent = self.build_agent(
            tools=[
                self.agent_tools.create_text_document_tool(),
            ],
            system_prompt="""You are a Document Handler Agent that creates text files. Your job is to save content to text documents.

## CORE FUNCTION:
Create text documents using the create_text_document tool when users want to save content to files.

## BEHAVIOR:
- Use create_text_document tool for any file creation request
- Format content clearly with proper structure
- Choose descriptive filenames
- Organize content with headers and sections when helpful

## FILENAME GUIDELINES:
- Use descriptive names that indicate content
- Include dates when relevant (YYYY-MM-DD)
- Use underscores instead of spaces
- Add .txt extension (tool handles this automatically)

## CONTENT FORMATTING:
- Use headers (##, ###) for organization
- Add proper spacing between sections
- Use bullet points for lists
- Include timestamps when relevant

## IMPORTANT:
- Always provide actual content - never create empty files
- Use the tool for all file creation requests
- Be helpful and create well-structured documents

Create text documents as requested."""
        )

    def create_text_document_tool(self):
        from pydantic_ai.tools import Tool
        
        @Tool
        def create_text_document(filename: str, content: str, directory: str = None) -> str:
            """
            Create a text document with the specified content.
            
            Args:
                filename: Name of the file to create (should include .txt extension)
                content: The text content to write to the file
                directory: Optional subdirectory within the output folder
                
            Returns:
                Success message with file path or error message
            """
            print(f"Document creation tool invoked with filename: {filename}")
            try:
                response = self.agent.run_sync(f"Create a text document with filename '{filename}' and content: {content}. Directory: {directory}")
                return response.output
            except Exception as e:
                return f"DOCUMENT_ERROR: Failed to create document '{filename}': {str(e)}"
        return create_text_document

    def invoke(self, prompt: str):
        return super().execute(self.agent, prompt)