# Agentic System 🤖

A multi-agent AI system built with FastAPI and Pydantic AI. Create custom AI agents with tools, orchestrate complex tasks, and integrate with platforms like Slack.

> **API Reference:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## Features

- **Multi-Agent Orchestration** — Coordinated AI agents with tool access
- **Flexible LLM Support** — Ollama (local) or OpenAI (cloud)
- **Platform Integrations** — Slack (live), WhatsApp/Email (planned)
- **Secure by Design** — API key auth, user isolation, bcrypt passwords

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                  │
├─────────────┬─────────────────┬────────────────────────┤
│ Auth Router │  Agent Router   │  Integration Router    │
├─────────────┼─────────────────┼────────────────────────┤
│ Auth Service│ Orchestrator    │  Slack Controller      │
│             │       │         │                        │
│             │   ┌───┴───┐     │                        │
│             │   ▼       ▼     │                        │
│             │ Web    Document │                        │
│             │ Agent   Agent   │                        │
│             │   └───┬───┘     │                        │
│             │       ▼         │                        │
│             │ Tool Registry   │                        │
│             │ (web_search,    │                        │
│             │  create_doc...) │                        │
└─────────────┴────────┬────────┴────────────────────────┘
                       ▼
              SQLite (SQLModel)
```

### Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | FastAPI + Pydantic AI |
| Database | SQLite/SQLModel + Alembic |
| Auth | API Key (UUID) + bcrypt |
| LLM | Ollama / OpenAI |
| Search | Tavily API |

### Project Structure

```
Agentic-system/
├── core/
│   ├── api/              # Business logic (agents, users)
│   └── auth/             # API key validation, password utils
├── database/
│   ├── models/           # SQLModel schemas
│   └── migrations/       # Alembic migrations
├── models/               # Pydantic DTOs
├── routers/              # API endpoints
├── services/
│   ├── agent_orchestrator.py
│   ├── tools.py
│   ├── agents/           # Web search, document handler
│   └── integrations/     # Slack
├── output/               # Generated documents
└── main.py
```

---

## Current Status

### ✅ Implemented

**User Management**
- Full CRUD with bcrypt passwords
- API key generation & validation
- Resource isolation per user

**Agent System**
- Create agents with custom tools & prompts
- Intelligent task routing via orchestrator
- Per-agent LLM provider selection

**Available Tools**

| Tool | Description |
|------|-------------|
| `web_search` | Tavily-powered web search |
| `create_document` | Generate text documents |
| `read_pdf` | Extract PDF text |
| `create_text_file` | Create/save text files |

**Integrations**
- Slack: Event listener, message handling, bot responses

---

## Quick Start

### Prerequisites
- Python 3.12+
- Ollama (optional, for local LLM)
- Tavily API key

### Setup

```bash
# Install
git clone <repo-url> && cd Agentic-system
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure .env
OLLAMA_MODEL=llama3.1
OLLAMA_BASE_URL=http://localhost:11434
TAVILY_API_KEY=your_key
DATABASE_URL=sqlite:///./agentic_system.db

# Initialize & run
alembic upgrade head
uvicorn main:app --reload
```

### Test It

```bash
# Create user → get API key
curl -X POST "http://localhost:8000/users/create" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","password":"test123"}'

# Create agent
curl -X POST "http://localhost:8000/agent/create" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Bot","description":"Research","system_prompt":"You help with research","tools":["web_search"]}'

# Invoke
curl -X POST "http://localhost:8000/agent/invoke" \
  -H "x-api-key: YOUR_API_KEY" -H "agent-id: YOUR_AGENT_ID" \
  -H "Content-Type: application/json" \
  -d '{"message":"Search for AI news"}'
```

**Docs:** http://localhost:8000/docs

---

## Roadmap

### Phase 1: Agent Intelligence *(Next)*
- [ ] Agent-to-agent communication
- [ ] Shared memory & context
- [ ] Multi-turn conversations
- [ ] Task queue (Celery/Redis)

### Phase 2: Integrations
- [ ] WhatsApp Business API
- [ ] Email (SMTP/SendGrid)
- [ ] Discord bot
- [ ] Google Calendar

### Phase 3: Advanced Capabilities
- [ ] Image generation (DALL-E/SD)
- [ ] Voice (TTS/STT)
- [ ] Excel/CSV processing
- [ ] SQL query generation

### Phase 4: Production
- [ ] PostgreSQL migration
- [ ] JWT + OAuth2
- [ ] Rate limiting
- [ ] Docker + K8s deployment
- [ ] Monitoring (Prometheus/Grafana)

---

## Security

**Implemented:**
- UUID API keys with bcrypt passwords
- User-scoped resource access
- Parameterized queries (SQL injection protection)
- Pydantic validation

**Best Practices:**
- Store secrets in env vars
- Use HTTPS in production
- Rotate API keys periodically
- Enable rate limiting

---

## Contributing

1. Fork → feature branch → PR
2. Follow PEP 8 + type hints
3. Update tests & docs

**Areas:** New agents, integrations, security, performance

---

## Resources

- [Pydantic AI](https://ai.pydantic.dev/) — Agent framework
- [FastAPI](https://fastapi.tiangolo.com/) — Web framework
- [Ollama](https://ollama.ai/) — Local LLMs
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic

---

**Built with ❤️ for exploring agentic AI systems**
