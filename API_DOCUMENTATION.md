# API Documentation

Complete API reference for the Agentic System. For general system information, see the [README](README.md).

## 📋 Table of Contents

- [Authentication](#authentication)
- [User Management](#user-management)
- [Agent Operations](#agent-operations)
- [Integrations](#integrations)
- [Error Handling](#error-handling)
- [Rate Limits](#rate-limits)

## 🔐 Authentication

All authenticated endpoints require an API key in the request header.

### Headers

```
x-api-key: your-api-key-here
```

For agent-specific operations, you'll also need:

```
agent-id: agent-uuid-here
```

### Getting Your API Key

1. Create a user account
2. Login with your credentials
3. Use the returned API key for subsequent requests

---

## 👥 User Management

### Create User

Create a new user account and receive an API key.

**Endpoint:** `POST /users/create`

**Authentication:** Not required

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "api_key": "123e4567-e89b-12d3-a456-426614174000",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/users/create" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "password": "securepassword123"
     }'
```

---

### Login

Authenticate and retrieve your API key.

**Endpoint:** `POST /auth/login`

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "api_key": "123e4567-e89b-12d3-a456-426614174000"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "john@example.com",
       "password": "securepassword123"
     }'
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials

---

### Get User

Retrieve user information by ID.

**Endpoint:** `GET /users/get/{user_id}`

**Authentication:** Not required (⚠️ Consider adding authentication)

**Path Parameters:**
- `user_id` (string, UUID): The user's unique identifier

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/users/get/550e8400-e29b-41d4-a716-446655440000"
```

---

### Get All Users

Retrieve a list of all users.

**Endpoint:** `GET /users/get-all`

**Authentication:** Not required (⚠️ Consider adding authentication)

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "is_active": true,
    "created_at": "2024-01-16T09:20:00Z",
    "updated_at": "2024-01-16T09:20:00Z"
  }
]
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/users/get-all"
```

---

### Update User

Update user information.

**Endpoint:** `PATCH /users/update/{user_id}`

**Authentication:** Not required (⚠️ Consider adding authentication)

**Path Parameters:**
- `user_id` (string, UUID): The user's unique identifier

**Request Body:** (all fields optional)
```json
{
  "name": "John Updated",
  "email": "john.updated@example.com",
  "password": "newpassword123",
  "is_active": false
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Updated",
  "email": "john.updated@example.com",
  "is_active": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:45:00Z"
}
```

**cURL Example:**
```bash
curl -X PATCH "http://localhost:8000/users/update/550e8400-e29b-41d4-a716-446655440000" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Updated"
     }'
```

---

### Delete User

Delete a user account.

**Endpoint:** `DELETE /users/delete/{user_id}`

**Authentication:** Not required (⚠️ Consider adding authentication)

**Path Parameters:**
- `user_id` (string, UUID): The user's unique identifier

**Response:** `200 OK`
```json
{
  "message": "User deleted successfully"
}
```

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/users/delete/550e8400-e29b-41d4-a716-446655440000"
```

---

## 🤖 Agent Operations

All agent endpoints require authentication via the `x-api-key` header.

### Create Agent

Create a new AI agent with custom configuration.

**Endpoint:** `POST /agent/create`

**Authentication:** Required

**Headers:**
```
x-api-key: your-api-key-here
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Research Assistant",
  "description": "An agent specialized in web research and documentation",
  "system_prompt": "You are a helpful research assistant that excels at finding information online and creating well-structured documents. Always cite your sources and provide accurate information.",
  "tools": ["web_search", "create_document"],
  "provider": "ollama"
}
```

**Field Descriptions:**
- `name` (string, required): Agent display name
- `description` (string, required): Brief description of agent's purpose
- `system_prompt` (string, required): Instructions that define agent behavior
- `tools` (array, required): List of tool names the agent can use
  - Available tools: `web_search`, `create_document`, `read_pdf`, `create_text_file`
- `provider` (string, optional): LLM provider (`ollama`, `openai`, etc.)

**Response:** `201 Created`
```json
{
  "id": "agent-550e8400-e29b-41d4-a716-446655440000",
  "name": "Research Assistant",
  "description": "An agent specialized in web research and documentation",
  "system_prompt": "You are a helpful research assistant...",
  "tools": ["web_search", "create_document"],
  "provider": "ollama",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/agent/create" \
     -H "x-api-key: your-api-key-here" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Research Assistant",
       "description": "An agent specialized in web research and documentation",
       "system_prompt": "You are a helpful research assistant...",
       "tools": ["web_search", "create_document"],
       "provider": "ollama"
     }'
```

---

### Invoke Agent

Execute an agent with a prompt/task.

**Endpoint:** `POST /agent/invoke`

**Authentication:** Required

**Headers:**
```
x-api-key: your-api-key-here
agent-id: agent-uuid-here
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "Search for the latest AI developments in 2024 and create a summary document"
}
```

**Response:** `200 OK`
```json
{
  "message": "I've completed your request. I searched for the latest AI developments in 2024 and created a comprehensive summary document. The document includes:\n\n1. Breakthrough in GPT-4 multimodal capabilities\n2. Advances in open-source LLMs\n3. AI regulation updates across major economies\n4. New developments in AI safety research\n\nThe document has been saved to 'output/AI_Developments_2024_Summary.txt' with full details and source citations."
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/agent/invoke" \
     -H "x-api-key: your-api-key-here" \
     -H "agent-id: agent-550e8400-e29b-41d4-a716-446655440000" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Search for the latest AI developments and create a summary"
     }'
```

**Example Tasks:**

1. **Web Research:**
```json
{
  "message": "Find information about quantum computing breakthroughs in 2024"
}
```

2. **Document Creation:**
```json
{
  "message": "Create a document explaining the basics of machine learning"
}
```

3. **Complex Multi-Step:**
```json
{
  "message": "Research renewable energy trends, compare with fossil fuels, and generate an analysis report with charts"
}
```

---

### Get Agent

Retrieve agent details by ID.

**Endpoint:** `GET /agent/get/{agent_id}`

**Authentication:** Required

**Headers:**
```
x-api-key: your-api-key-here
```

**Path Parameters:**
- `agent_id` (string, UUID): The agent's unique identifier

**Response:** `200 OK`
```json
{
  "id": "agent-550e8400-e29b-41d4-a716-446655440000",
  "name": "Research Assistant",
  "description": "An agent specialized in web research and documentation",
  "system_prompt": "You are a helpful research assistant...",
  "tools": ["web_search", "create_document"],
  "provider": "ollama",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/agent/get/agent-550e8400-e29b-41d4-a716-446655440000" \
     -H "x-api-key: your-api-key-here"
```

---

### Get All Agents

Retrieve all agents belonging to the authenticated user.

**Endpoint:** `GET /agent/get-all`

**Authentication:** Required

**Headers:**
```
x-api-key: your-api-key-here
```

**Response:** `200 OK`
```json
[
  {
    "id": "agent-550e8400-e29b-41d4-a716-446655440000",
    "name": "Research Assistant",
    "description": "Web research and documentation",
    "system_prompt": "You are a helpful research assistant...",
    "tools": ["web_search", "create_document"],
    "provider": "ollama",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
  },
  {
    "id": "agent-660e8400-e29b-41d4-a716-446655440001",
    "name": "Data Analyzer",
    "description": "Data analysis and visualization",
    "system_prompt": "You are a data analyst...",
    "tools": ["web_search", "create_document"],
    "provider": "openai",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-01-16T09:30:00Z",
    "updated_at": "2024-01-16T09:30:00Z"
  }
]
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/agent/get-all" \
     -H "x-api-key: your-api-key-here"
```

---

### Update Agent

Update an existing agent's configuration.

**Endpoint:** `PATCH /agent/update/{agent_id}`

**Authentication:** Required

**Headers:**
```
x-api-key: your-api-key-here
Content-Type: application/json
```

**Path Parameters:**
- `agent_id` (string, UUID): The agent's unique identifier

**Request Body:** (all fields optional)
```json
{
  "name": "Advanced Research Assistant",
  "description": "Enhanced web research with advanced capabilities",
  "system_prompt": "You are an advanced research assistant with expertise in academic research...",
  "tools": ["web_search", "create_document", "read_pdf"],
  "provider": "openai"
}
```

**Response:** `200 OK`
```json
{
  "id": "agent-550e8400-e29b-41d4-a716-446655440000",
  "name": "Advanced Research Assistant",
  "description": "Enhanced web research with advanced capabilities",
  "system_prompt": "You are an advanced research assistant...",
  "tools": ["web_search", "create_document", "read_pdf"],
  "provider": "openai",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-16T10:15:00Z"
}
```

**cURL Example:**
```bash
curl -X PATCH "http://localhost:8000/agent/update/agent-550e8400-e29b-41d4-a716-446655440000" \
     -H "x-api-key: your-api-key-here" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Advanced Research Assistant",
       "tools": ["web_search", "create_document", "read_pdf"]
     }'
```

---

### Delete Agent

Delete an agent.

**Endpoint:** `DELETE /agent/delete/{agent_id}`

**Authentication:** Required

**Headers:**
```
x-api-key: your-api-key-here
```

**Path Parameters:**
- `agent_id` (string, UUID): The agent's unique identifier

**Response:** `200 OK`
```json
{
  "message": "Agent deleted successfully"
}
```

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/agent/delete/agent-550e8400-e29b-41d4-a716-446655440000" \
     -H "x-api-key: your-api-key-here"
```

---

## 🔌 Integrations

### Slack Event Listener

Webhook endpoint for receiving Slack events.

**Endpoint:** `POST /integrations/slack/listener`

**Authentication:** Verified via Slack signing secret

**Headers:**
```
X-Slack-Signature: slack-signature
X-Slack-Request-Timestamp: timestamp
Content-Type: application/json
```

**Request Body (URL Verification Challenge):**
```json
{
  "type": "url_verification",
  "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P",
  "token": "Jhj5dZrVaK7ZwHHjRyZWjbDl"
}
```

**Response:** `200 OK`
```json
{
  "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P"
}
```

**Request Body (Event Callback):**
```json
{
  "type": "event_callback",
  "event": {
    "type": "message",
    "user": "U061F7AUR",
    "text": "Hello bot!",
    "channel": "C0LAN2Q65",
    "ts": "1515449522.000016"
  }
}
```

**Setup Instructions:**

1. Create a Slack App at [api.slack.com/apps](https://api.slack.com/apps)
2. Enable Event Subscriptions
3. Set Request URL to: `https://your-domain.com/integrations/slack/listener`
4. Subscribe to bot events: `message.channels`, `message.im`, `app_mention`
5. Install app to workspace
6. Add credentials to `.env`:
   ```env
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_SIGNING_SECRET=your-signing-secret
   ```

---

## 🏥 System Health

### Health Check

Check API availability and status.

**Endpoint:** `GET /health`

**Authentication:** Not required

**Response:** `200 OK`
```json
{
  "message": "OK"
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/health"
```

---

## ⚠️ Error Handling

### Standard Error Response

All endpoints return errors in the following format:

```json
{
  "detail": "Error message description"
}
```

### HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Request succeeded |
| `201 Created` | Resource created successfully |
| `400 Bad Request` | Invalid request parameters |
| `401 Unauthorized` | Invalid or missing API key |
| `403 Forbidden` | Insufficient permissions |
| `404 Not Found` | Resource not found |
| `422 Unprocessable Entity` | Validation error |
| `500 Internal Server Error` | Server error |

### Common Error Examples

**Invalid API Key:**
```json
{
  "detail": "Invalid API key"
}
```

**Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

**Not Found:**
```json
{
  "detail": "Agent not found"
}
```

**Unauthorized Access:**
```json
{
  "detail": "You don't have permission to access this agent"
}
```

---

## 🚦 Rate Limits

**Current Status:** No rate limiting implemented

**Planned Implementation:**
- Rate limiting per API key
- Different tiers based on usage
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## 📚 Interactive Documentation

The API provides interactive documentation powered by OpenAPI/Swagger:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Use these interfaces to:
- Explore all endpoints
- Test API calls directly from the browser
- View request/response schemas
- Download OpenAPI specification

---

## 🔗 Additional Resources

- [Main Documentation](README.md) - System overview and setup
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Framework reference
- [Pydantic AI](https://ai.pydantic.dev/) - Agent framework

---

**Need help?** Open an issue on GitHub or check the interactive documentation at `/docs`.

