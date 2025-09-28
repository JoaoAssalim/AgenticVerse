# Agentic System

A personal project exploring the implementation of agentic systems, local LLMs, and AI news aggregation. This project aims to build a multi-agent system capable of searching information, creating documents, and integrating with various communication platforms like WhatsApp, email, and other tools.

## 🎯 Project Vision

The main goal is to create an intelligent system that can:
- **Search and aggregate information** from various sources
- **Generate and manage documents** automatically
- **Integrate with communication platforms** (WhatsApp, Email, etc.)
- **Leverage local LLMs** for privacy and cost efficiency
- **Implement multi-agent architectures** for complex task orchestration

## 🏗️ Current Architecture

### Core Components

- **FastAPI Backend**: RESTful API for agent interactions
- **Pydantic AI Framework**: Agent orchestration and tool management
- **Ollama Integration**: Local LLM support for privacy and cost control
- **Tavily Search**: Real-time web search capabilities
- **Document Generation**: Automated text file creation and management

### Project Structure

```
Agentic-system/
├── core/                    # Core system components
├── models/                  # Data models and schemas
├── routers/                 # FastAPI route handlers
│   └── agent.py            # Agent interaction endpoints
├── services/                # Business logic services
│   └── artificial_intelligence.py  # AI agent implementation
├── output/                  # Generated documents and files
├── main.py                  # FastAPI application entry point
└── requirements.txt         # Python dependencies
```

## 🚀 Features

### ✅ Currently Implemented

- **AI Agent with Tools**: Intelligent agent with web search and document creation capabilities
- **Web Search Integration**: Real-time information retrieval using Tavily API
- **Document Generation**: Automated creation of text files with AI-generated content
- **Local LLM Support**: Integration with Ollama for running models locally
- **RESTful API**: FastAPI-based endpoints for agent interactions
- **Health Monitoring**: System health check endpoint

### 🔄 In Development

- Multi-agent orchestration
- WhatsApp integration
- Email automation
- Advanced document processing
- Task scheduling and automation

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.12+
- Ollama (for local LLM support)
- Tavily API key (for web search)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Agentic-system
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OLLAMA_MODEL=llama3.1  # or your preferred model
   OLLAMA_BASE_URL=http://localhost:11434
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

5. **Start Ollama (if using local models)**
   ```bash
   ollama serve
   ollama pull llama3.1  # or your preferred model
   ```

6. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Endpoints

- **GET** `/health` - Health check endpoint
- **POST** `/agent/invoke` - Invoke the AI agent with a prompt

### Example Usage

```bash
# Health check
curl http://localhost:8000/health

# Invoke agent
curl -X POST "http://localhost:8000/agent/invoke" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Search for latest AI news and create a summary document"}'
```

## 🤖 Agent Capabilities

The current AI agent can:

1. **Search the Web**: Use Tavily search to find real-time information
2. **Create Documents**: Generate and save text files with structured content
3. **Process Information**: Analyze and format search results into readable documents
4. **Local Processing**: Run entirely on local infrastructure using Ollama

### Example Agent Tasks

- "Search for the latest AI developments and create a news summary"
- "Find information about the World Cup history and save it to a file"
- "Research renewable energy trends and generate a report"

## 🔮 Roadmap

### Phase 1: Core Multi-Agent System
- [ ] Implement agent communication protocols
- [ ] Add task distribution and load balancing
- [ ] Create specialized agents for different domains

### Phase 2: Communication Integrations
- [ ] WhatsApp Business API integration
- [ ] Email automation (SMTP/SendGrid)
- [ ] Slack/Discord bot support
- [ ] SMS notifications

### Phase 3: Advanced Features
- [ ] Document processing (PDF, Word, etc.)
- [ ] Image generation and analysis
- [ ] Voice synthesis and recognition
- [ ] Calendar and scheduling integration

### Phase 4: Intelligence & Automation
- [ ] Task scheduling and cron jobs
- [ ] Workflow automation
- [ ] Learning and adaptation mechanisms
- [ ] Performance monitoring and analytics

## 🛡️ Privacy & Security

- **Local LLM Support**: Process sensitive data locally without external API calls
- **Environment Variables**: Secure API key management
- **Input Validation**: Robust input sanitization and validation
- **Error Handling**: Comprehensive error management and logging

## 🤝 Contributing

This is a personal project for learning and experimentation. Feel free to:
- Fork the repository
- Submit issues and feature requests
- Create pull requests for improvements
- Share ideas and feedback

## 📄 License

This project is for educational and personal use. Please respect the terms of service of integrated APIs and services.

## 🔗 Resources

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Tavily API Documentation](https://tavily.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

*Built with ❤️ for exploring the future of agentic AI systems*
