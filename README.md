# AI Agents Backend

Backend service for AI agents using ADK (Agent Development Kit). This service provides AI agent capabilities and connects to Google's API internally.

## 🚀 How to Run

### Prerequisites
- Docker and Docker Compose
- Google API Key
- **Serverless MCP Server** running (HTTP) - [AI Agents MCP Server](http://github.com/ailtonacr/ai-agents-mcp-server)

### Quick Setup

1. **Configure environment variables:**
   Create a `.env` file in the project root with:
   ```bash
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=your_google_api_key
   # MCP HTTP server settings
   MCP_SERVER_HOST=your_mcp_server_host
   MCP_SERVER_PORT=your_mcp_server_port
   ```

2. **Run with Docker:**
   ```bash
   make docker-run
   ```

3. **Access the service:**
   - ADK Web Interface: http://localhost:8000

### Stop the Application
```bash
make docker-stop
```

## 📋 Features

- **ADK Web Interface**: Built-in web interface for agent interaction
- **Google API Integration**: Connects to Google's AI services
- **Agent Management**: Support for multiple AI agents (Bibble agent included)
- **Serverless MCP Integration**: Communicates with external MCP server over HTTP for tool execution

## 🔧 Local Development

If you prefer to run without Docker, ensure the serverless MCP HTTP server is running and then:

```bash
# Install dependencies
make setup

# Configure .env as above

# Start ADK Web Interface
cd src/agents
adk web --host 0.0.0.0 --port 8000
```

## 🏗️ Project Structure

- `src/agents/` - AI agent implementations
- `src/mcp_server/` - Model Context Protocol server
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Multi-container setup

## 📝 Available Commands

- `make help` - Show available commands
- `make setup` - Install dependencies
- `make docker-run` - Run with Docker
- `make docker-stop` - Stop Docker containers
- `make lint` - Format code with Black
- `make test` - Run unit tests with coverage
