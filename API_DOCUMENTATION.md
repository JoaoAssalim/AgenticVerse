# API Documentation

Base URL: `http://localhost:8000`

## Authentication

```
x-api-key: your-api-key
agent-id: agent-uuid  # (agent operations only)
```

---

## User Endpoints

### Create User
`POST /users/create` — No auth required

```json
// Request
{ "name": "John Doe", "email": "john@example.com", "password": "securepassword123" }

// Response 201
{ "id": "uuid", "name": "John Doe", "email": "john@example.com", "api_key": "uuid", "is_active": true, "created_at": "...", "updated_at": "..." }
```

### Login
`POST /auth/login` — No auth required

```json
// Request
{ "email": "john@example.com", "password": "securepassword123" }

// Response 200
{ "api_key": "uuid" }
```

### Get User
`GET /users/get/{user_id}`

### Get All Users
`GET /users/get-all`

### Update User
`PATCH /users/update/{user_id}`

```json
// Request (all fields optional)
{ "name": "...", "email": "...", "password": "...", "is_active": false }
```

### Delete User
`DELETE /users/delete/{user_id}`

---

## Agent Endpoints

All require `x-api-key` header.

### Create Agent
`POST /agent/create`

```json
// Request
{
  "name": "Research Assistant",
  "description": "Web research and documentation",
  "system_prompt": "You are a helpful research assistant...",
  "tools": ["web_search", "create_document"],
  "provider": "ollama"  // optional: ollama, openai
}

// Response 201
{ "id": "agent-uuid", "name": "...", "tools": [...], "user_id": "...", ... }
```

**Available Tools:** `web_search`, `create_document`, `read_pdf`, `create_text_file`

### Invoke Agent
`POST /agent/invoke` — Requires `agent-id` header

```json
// Request
{ "message": "Search for AI developments and create a summary" }

// Response 200
{ "message": "I've completed your request..." }
```

### Get Agent
`GET /agent/get/{agent_id}`

### Get All Agents
`GET /agent/get-all`

### Update Agent
`PATCH /agent/update/{agent_id}`

```json
// Request (all fields optional)
{ "name": "...", "description": "...", "system_prompt": "...", "tools": [...], "provider": "..." }
```

### Delete Agent
`DELETE /agent/delete/{agent_id}`

---

## Integrations

### Slack Listener
`POST /integrations/slack/listener`

Webhook for Slack events. Configure in Slack App settings:
- Request URL: `https://your-domain.com/integrations/slack/listener`
- Bot events: `message.channels`, `message.im`, `app_mention`

**Environment:**
```env
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
```

---

## Health Check

`GET /health` → `{ "message": "OK" }`

---

## Error Responses

```json
{ "detail": "Error message" }
```

| Code | Meaning |
|------|---------|
| 400 | Bad request |
| 401 | Invalid/missing API key |
| 403 | Forbidden |
| 404 | Not found |
| 422 | Validation error |
| 500 | Server error |

---

## Interactive Docs

- Swagger UI: [/docs](http://localhost:8000/docs)
- ReDoc: [/redoc](http://localhost:8000/redoc)
