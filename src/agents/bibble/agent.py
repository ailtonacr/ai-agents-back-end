from google.adk.agents import Agent
from .prompts import (
    BIBBLE_PROMPT, BIBBLE_DESCRIPTION, BIBBLE_MODEL,
    PLAY_MIND_PROMPT, PLAY_MIND_MODEL, PLAY_MIND_DESCRIPTION
)
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from pathlib import Path

MCP_SERVER_SCRIPT = str((Path(__file__).parent.parent.parent / "mcp_server" / "server.py").resolve())


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
            connection_params=StdioServerParameters(
                command="python3",
                args=[MCP_SERVER_SCRIPT],
            )
        )
    ],
)
