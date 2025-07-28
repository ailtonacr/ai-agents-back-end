from google.adk.agents import Agent
from .prompts import (
    BIBBLE_PROMPT, BIBBLE_DESCRIPTION, BIBBLE_MODEL,
    PLAY_MIND_PROMPT, PLAY_MIND_MODEL, PLAY_MIND_DESCRIPTION
)
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
import os

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost")
MCP_SERVER_PORT = os.getenv("MCP_SERVER_PORT", "8001")

playMind = Agent(
    model=PLAY_MIND_MODEL,
    name="PlayMind",
    description=PLAY_MIND_DESCRIPTION,
    instruction=PLAY_MIND_PROMPT
)


root_agent = Agent(
    model=BIBBLE_MODEL,
    name="Bibble",
    description=BIBBLE_DESCRIPTION,
    instruction=BIBBLE_PROMPT,
    sub_agents=[playMind],
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=f'{MCP_SERVER_URL}:{MCP_SERVER_PORT}/mcp'
            )
        )
    ],
)
