# Agentic System 🤖

A comprehensive multi-agent AI system built with FastAPI and Pydantic AI, featuring intelligent orchestration, robust authentication, and seamless platform integrations.

> **📚 Complete API Reference:** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed endpoint documentation and examples.

---

## 📖 Table of Contents

- [Overview](#-overview)
- [What's Been Built](#-whats-been-built)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [What's Next](#-whats-next)
- [Contributing](#-contributing)

---

## 🎯 Overview

This project implements a production-ready agentic AI system designed for:

- 🧠 **Intelligent Multi-Agent Orchestration** - Coordinated AI agents working together
- 🔐 **Enterprise-Grade Security** - API key authentication with user isolation
- 🌐 **Real-Time Intelligence** - Live web search and information aggregation
- 📄 **Document Processing** - Automated creation and analysis of documents
- 🔌 **Platform Integrations** - Slack (implemented), WhatsApp, Email (planned)
- 🏠 **Privacy-First** - Local LLM support via Ollama for sensitive data

### Core Philosophy

Build a flexible, extensible agent framework that can:
- Solve complex tasks through agent collaboration
- Maintain security and data isolation between users
- Integrate seamlessly with existing communication platforms
- Process data locally when privacy is paramount
- Scale from personal projects to production workloads

---

## ✅ What's Been Built

### 🔐 Authentication & User Management

**Fully Implemented**

- ✅ Complete user lifecycle (create, read, update, delete)
- ✅ Secure password hashing with bcrypt
- ✅ UUID-based API key generation and validation
- ✅ Email/password login system
- ✅ API key-based authentication for all protected endpoints
- ✅ User resource isolation (users can only access their own agents)

**Technical Stack:**
- FastAPI Security with `APIKeyHeader`
- SQLModel for database operations
- bcrypt for password hashing

---

### 🤖 Multi-Agent System

**Fully Implemented**

#### Agent Orchestrator
- ✅ Intelligent task routing and delegation
- ✅ Dynamic tool assignment based on agent configuration
- ✅ Multi-agent coordination
- ✅ User-scoped agent management

#### Specialized Agents
1. **Web Search Agent**
   - Real-time web search via Tavily API
   - Multi-result aggregation with source attribution
   - Configurable search parameters
   
2. **Document Handler Agent**
   - PDF text extraction and processing
   - Text file creation with custom formatting
   - Document summarization
   - Multi-format support (PDF, TXT)
   
3. **Base Agent**
   - Extensible foundation for custom agents
   - Tool registry system
   - Configurable LLM providers

#### Agent Management
- ✅ Create custom agents with specific tools and prompts
- ✅ Update agent configurations on the fly
- ✅ User-scoped agent ownership
- ✅ Per-agent provider selection (Ollama, OpenAI, etc.)

---

### 🔧 Available Tools

Agents can be equipped with the following tools:

| Tool | Description | Status |
|------|-------------|--------|
| `web_search` | Tavily-powered real-time web search | ✅ Live |
| `create_document` | Generate formatted text documents | ✅ Live |
| `read_pdf` | Extract text from PDF files | ✅ Live |
| `create_text_file` | Create and save text files | ✅ Live |

---

### 🔌 Platform Integrations

#### Slack Integration (Implemented)
- ✅ Event listener webhook
- ✅ URL verification challenge handling
- ✅ Message event processing
- ✅ Bot response system

**Setup:** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md#slack-event-listener)

---

### 💾 Database & Migrations

**Fully Implemented**

- ✅ SQLModel (SQLAlchemy) ORM
- ✅ Alembic migration system
- ✅ Database models:
  - `users` - User accounts and authentication
  - `agents` - Agent configurations
  - `integrations` - External platform connections
- ✅ Foreign key relationships (agents → users)
- ✅ UUID primary keys
- ✅ Automatic timestamps

---

## 🏗️ Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────┐
│                   FastAPI Application               │
│                                                     │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │   Auth     │  │    Agent     │  │ Integration │  │
│  │  Router    │  │   Router     │  │   Router    │  │
│  └────────────┘  └──────────────┘  └─────────────┘  │
│         │                │                  │       │
│         ▼                ▼                  ▼       │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │   Auth     │  │    Agent     │  │    Slack    │  │
│  │  Service   │  │ Orchestrator │  │ Controller  │  │
│  └────────────┘  └──────────────┘  └─────────────┘  │
│                          │                          │
│              ┌───────────┴───────────┐              │
│              ▼                       ▼              │
│    ┌──────────────────┐    ┌──────────────────┐     │
│    │  Web Search      │    │ Document Handler │     │
│    │     Agent        │    │      Agent       │     │
│    └──────────────────┘    └──────────────────┘     │
│              │                       │              │
│              ▼                       ▼              │
│    ┌──────────────────────────────────────────┐     │
│    │          Tool Registry                   │     │
│    │  (web_search, create_document, etc.)     │     │
│    └──────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │  SQLite Database │
              │  (via SQLModel)  │
              └──────────────────┘
```

### Technology Stack

| Layer | Technology |
|-------|-----------|
| **Web Framework** | FastAPI |
| **AI Framework** | Pydantic AI |
| **Database** | SQLite (SQLModel/SQLAlchemy ORM) |
| **Migrations** | Alembic |
| **Authentication** | API Key (UUID) + bcrypt |
| **LLM Providers** | Ollama (local) / OpenAI (cloud) |
| **Web Search** | Tavily API |
| **Integrations** | Slack Web API |

### Project Structure

```
Agentic-system/
├── core/                      # Core functionality
│   ├── api/                  # Business logic layer
│   │   ├── agents.py        # Agent CRUD operations
│   │   └── users.py         # User CRUD operations
│   └── auth/                # Authentication
│       ├── auth.py          # API key validation
│       └── utils.py         # Password utilities
│
├── database/                 # Data layer
│   ├── config.py            # DB connection setup
│   ├── models/              # SQLModel schemas
│   │   ├── users.py        # User model
│   │   ├── agent.py        # Agent model
│   │   ├── integrations.py # Integration model
│   │   └── base.py         # Base model
│   └── migrations/         # Alembic migrations
│
├── models/                   # API DTOs (Pydantic)
│   ├── users.py            # User request/response models
│   ├── agent.py            # Agent request/response models
│   └── headers.py          # Common headers
│
├── routers/                  # API endpoints
│   ├── auth.py             # Login endpoint
│   ├── users.py            # User management
│   ├── agent.py            # Agent operations
│   └── integrations.py     # Platform integrations
│
├── services/                 # Business logic
│   ├── agent_orchestrator.py  # Agent coordination
│   ├── tools.py               # Shared tools
│   ├── agents/                # Agent implementations
│   │   ├── base_agent.py
│   │   ├── web_search_agent.py
│   │   └── document_handler_agent.py
│   └── integrations/          # Platform integrations
│       └── slack/
│           ├── controller.py  # Event handling
│           └── handler.py     # Message processing
│
├── output/                    # Generated documents
├── main.py                   # Application entry point
├── alembic.ini              # Alembic config
├── requirements.txt         # Dependencies
├── README.md               # This file
└── API_DOCUMENTATION.md    # Complete API reference
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Ollama (for local LLM support)
- Tavily API key ([get one here](https://tavily.com))

### Installation

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd Agentic-system
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   
   Create `.env` file:
   ```env
   # LLM Configuration
   OLLAMA_MODEL=llama3.1
   OLLAMA_BASE_URL=http://localhost:11434
   
   # API Keys
   TAVILY_API_KEY=your_tavily_api_key
   OPENAI_API_KEY=your_openai_key  # Optional
   
   # Database
   DATABASE_URL=sqlite:///./agentic_system.db
   ```

3. **Initialize database**
   ```bash
   alembic upgrade head
   ```

4. **Start Ollama** (if using local LLMs)
   ```bash
   ollama serve
   ollama pull llama3.1
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

Access the API at:
- **Application**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **API Reference**: http://localhost:8000/redoc

### Quick Test

```bash
# 1. Create a user
curl -X POST "http://localhost:8000/users/create" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"test123"}'

# 2. Login and get API key
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# 3. Create an agent
curl -X POST "http://localhost:8000/agent/create" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Research Bot",
    "description":"Web research assistant",
    "system_prompt":"You are a helpful research assistant",
    "tools":["web_search","create_document"],
    "provider":"ollama"
  }'

# 4. Use the agent
curl -X POST "http://localhost:8000/agent/invoke" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "agent-id: YOUR_AGENT_ID" \
  -H "Content-Type: application/json" \
  -d '{"message":"Search for AI news and create a summary"}'
```

For complete API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

---

## 🗓️ What's Next

### 🚧 Phase 2: Enhanced Multi-Agent System

**Goals:** Advanced agent collaboration and intelligence

- [ ] **Agent Communication**
  - Inter-agent messaging protocol
  - Shared context and memory
  - Agent-to-agent task delegation
  
- [ ] **Task Management**
  - Task queue system (Celery/Redis)
  - Job scheduling and cron integration
  - Background task processing
  - Task prioritization
  
- [ ] **Intelligence Features**
  - Agent learning and memory
  - Performance analytics per agent
  - Conversation history and context
  - Multi-turn conversations with state
  
- [ ] **Orchestration Strategies**
  - Voting and consensus mechanisms
  - Parallel agent execution
  - Fallback and retry logic
  - Load balancing across agents

**Timeline:** Q2 2024

---

### 📋 Phase 3: Advanced Platform Integrations

**Goals:** Expand communication channels and automate workflows

#### Email Automation
- [ ] SMTP server integration
- [ ] SendGrid/Mailgun support
- [ ] Email templates with variables
- [ ] Scheduled email campaigns
- [ ] Attachment handling (PDF, images)
- [ ] Email parsing and inbox monitoring

#### WhatsApp Integration
- [ ] WhatsApp Business API setup
- [ ] Message webhooks
- [ ] Media handling (images, documents, audio, video)
- [ ] Interactive messages (buttons, lists)
- [ ] WhatsApp templates
- [ ] Group chat support

#### Discord Bot
- [ ] Discord bot application
- [ ] Slash commands
- [ ] Event handling (messages, reactions)
- [ ] Channel and server management
- [ ] Embed messages with rich formatting
- [ ] Voice channel integration (future)

#### Calendar Integration
- [ ] Google Calendar API
- [ ] Microsoft Outlook/Office 365
- [ ] Event CRUD operations
- [ ] Meeting scheduling automation
- [ ] Reminder system
- [ ] Availability checking

**Timeline:** Q3 2024

---

### 🔮 Phase 4: Advanced AI Capabilities

**Goals:** Expand what agents can do

#### Document Processing
- [ ] Excel/CSV parsing and generation
- [ ] PowerPoint/slide generation
- [ ] Markdown to PDF conversion
- [ ] Code file analysis (syntax highlighting)
- [ ] Multi-document comparison
- [ ] Document translation

#### Image & Vision
- [ ] DALL-E/Stable Diffusion integration
- [ ] Image analysis and description
- [ ] OCR for text extraction
- [ ] Chart and diagram generation
- [ ] Image editing and manipulation
- [ ] Screenshot analysis

#### Voice & Audio
- [ ] Text-to-speech (ElevenLabs, OpenAI TTS)
- [ ] Speech-to-text (Whisper)
- [ ] Voice command processing
- [ ] Audio file transcription
- [ ] Multi-language support

#### Data & Analytics
- [ ] SQL query generation
- [ ] Database integration (PostgreSQL, MySQL)
- [ ] Data visualization (charts, graphs)
- [ ] Statistical analysis
- [ ] CSV/Excel data processing
- [ ] Business intelligence reports

**Timeline:** Q4 2024

---

### 🚀 Phase 5: Production Readiness

**Goals:** Scale and harden for production use

#### Scalability
- [ ] PostgreSQL migration for production
- [ ] Redis caching layer
- [ ] Celery for background tasks
- [ ] Database connection pooling
- [ ] Horizontal scaling support
- [ ] Load balancer configuration

#### Monitoring & Observability
- [ ] Structured logging (JSON logs)
- [ ] ELK stack (Elasticsearch, Logstash, Kibana)
- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring (APM)
- [ ] Uptime monitoring

#### Security Enhancements
- [ ] JWT token authentication
- [ ] OAuth2 integration (Google, GitHub)
- [ ] Role-based access control (RBAC)
- [ ] API rate limiting (per user/endpoint)
- [ ] Request throttling
- [ ] Audit logs
- [ ] IP whitelisting
- [ ] Two-factor authentication (2FA)

#### Developer Experience
- [ ] Python SDK
- [ ] JavaScript/TypeScript SDK
- [ ] Comprehensive test suite (pytest)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Docker containerization
- [ ] Docker Compose for local dev
- [ ] Kubernetes deployment manifests
- [ ] Terraform infrastructure as code

**Timeline:** Q1 2025

---

### 💡 Phase 6: Innovation & Advanced Features

**Goals:** Push the boundaries

- [ ] Fine-tuning custom models
- [ ] Multi-modal agent interactions
- [ ] Real-time streaming responses (WebSocket)
- [ ] Agent marketplace (share/discover agents)
- [ ] Visual workflow builder (no-code UI)
- [ ] Mobile app for agent management
- [ ] Browser extension
- [ ] Plugin system for custom tools
- [ ] GraphQL API
- [ ] Webhooks for events

**Timeline:** 2025+

---

## 🛡️ Security & Privacy

### Current Implementation

✅ **Authentication**
- UUID-based API keys
- Bcrypt password hashing
- Secure header-based auth

✅ **Authorization**
- User resource isolation
- User-scoped agent access
- Protected endpoints

✅ **Data Protection**
- SQLModel parameterized queries (SQL injection prevention)
- Pydantic validation (input sanitization)
- Environment variable management

### Privacy Features

- **Local LLM Support**: Process sensitive data locally with Ollama
- **Data Isolation**: Users can only access their own resources
- **No Third-Party Tracking**: No analytics beyond what you configure

### Best Practices

- 🔑 Store API keys in environment variables
- 🔄 Rotate API keys periodically
- 🔒 Use HTTPS in production
- 🚫 Never commit secrets to version control
- 📝 Implement rate limiting in production
- 🔍 Monitor and audit API usage

---

## 🤝 Contributing

This is a personal learning project, but contributions are welcome!

### How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add type hints to all functions
- Write docstrings for classes and functions
- Update tests for new features
- Update documentation

### Areas for Contribution

- 🤖 New agent types
- 🔌 Additional integrations
- ⚡ Performance optimizations
- 🔒 Security enhancements
- 📚 Documentation improvements
- 🐛 Bug fixes

---

## 📚 Documentation

- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference with examples
- **[Interactive API Docs](http://localhost:8000/docs)** - Swagger UI (when running)
- **[Alternative Docs](http://localhost:8000/redoc)** - ReDoc interface (when running)

---

## 🔗 Resources

### Frameworks & Libraries
- [Pydantic AI](https://ai.pydantic.dev/) - AI agent framework
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [SQLModel](https://sqlmodel.tiangolo.com/) - SQL database ORM
- [Alembic](https://alembic.sqlalchemy.org/) - Database migrations

### LLM Providers
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [OpenAI API](https://platform.openai.com/docs) - Cloud LLM

### APIs & Services
- [Tavily API](https://tavily.com/docs) - Web search
- [Slack API](https://api.slack.com/docs) - Slack integration

### Learning Resources
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) - Anthropic
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) - GitHub
- [Multi-Agent Systems](https://microsoft.github.io/autogen/) - Microsoft AutoGen

---

## 📄 License

This project is for educational and personal use. Please respect the terms of service of all integrated APIs and services.

---

## 🙏 Acknowledgments

Built with amazing open-source tools. Special thanks to:
- The FastAPI community
- Pydantic AI developers
- Ollama team for democratizing local LLMs
- All open-source contributors

---

**Built with ❤️ for exploring the future of agentic AI systems**

*Questions? Suggestions? Open an issue or start a discussion!*

🌟 **Star this repo if you find it useful!**
