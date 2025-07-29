from agno.agent import Agent
from agno.team.team import Team
from agno.playground import Playground
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory

from config import (
    BIBBLE_PROMPT, BIBBLE_DESCRIPTION, BIBBLE_MODEL,
    PLAY_MIND_PROMPT, PLAY_MIND_MODEL, PLAY_MIND_DESCRIPTION,
    COORDINATOR_PROMPT, COORDINATOR_DESCRIPTION, COORDINATOR_MODEL
)
from agno.tools.mcp import MCPTools, StreamableHTTPClientParams
import os

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost")
MCP_SERVER_PORT = os.getenv("MCP_SERVER_PORT", "8001")

SERVER_PARAMS = StreamableHTTPClientParams(
    url=f'{MCP_SERVER_URL}:{MCP_SERVER_PORT}/mcp'
)


# Create a memory instance with persistent storage
memory_db = SqliteMemoryDb(table_name="memory", db_file="memory.db")
memory = Memory(db=memory_db)


playMind = Agent(
    model=PLAY_MIND_MODEL,
    name="PlayMind",
    description=PLAY_MIND_DESCRIPTION,
    instructions=PLAY_MIND_PROMPT,
    markdown=True,
    memory=memory,
    enable_agentic_memory=True,
    enable_user_memories=True,
    add_history_to_messages=True,
    num_history_runs=5,
)


bibble = Agent(
    model=BIBBLE_MODEL,
    name="Bibble",
    description=BIBBLE_DESCRIPTION,
    instructions=BIBBLE_PROMPT,
    tools=[
        MCPTools(
            server_params=SERVER_PARAMS,
            transport="streamable-http"
        )
    ],
    markdown=True,
    memory=memory,
    enable_agentic_memory=True,
    enable_user_memories=True,
    add_history_to_messages=True,
    num_history_runs=5,
)

coordinator_team = Team(
    name="Coordenador geral",
    mode="coordinate",
    model=COORDINATOR_MODEL,
    members=[bibble, playMind],
    description=COORDINATOR_DESCRIPTION,
    instructions=COORDINATOR_PROMPT,
    markdown=True,
    memory=memory,
    enable_agentic_context=True,
    enable_agentic_memory=True,
    enable_user_memories=True,
    success_criteria="Coordenador geral deve coordenar as atividades do projeto Bibble, garantindo que todos os agentes estejam alinhados e trabalhando em conjunto.",
    add_datetime_to_instructions=True,
    enable_session_summaries=True,
    add_history_to_messages=True,
    num_history_runs=5,
)

playground = Playground(teams=[coordinator_team], agents=[bibble, playMind])
app = playground.get_app()


if __name__ == '__main__':
    playground.serve(app="agent:app", reload=True)
