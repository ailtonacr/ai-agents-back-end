import asyncio
import json

import mcp.server.stdio

from interfaces import (
    rag_finance_report_search,
    get_finance_report_filters
)

from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

from mcp import types as mcp_types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from infrastructure.logging_config import logger

logger.info("Creating MCP Server instance...")
app = Server("Servidor-mcp")

ADK_TOOLS = {
    "rag_finance_report_search": FunctionTool(func=rag_finance_report_search),
    "get_finance_report_filters": FunctionTool(func=get_finance_report_filters),
}


@app.list_tools()
async def list_mcp_tools() -> list[mcp_types.Tool]:
    """MCP handler to list tools this server exposes."""
    logger.info("MCP Server: Received list_tools request.")
    mcp_tools_list = []
    for tool_name, adk_tool_instance in ADK_TOOLS.items():
        if not adk_tool_instance.name:
            adk_tool_instance.name = tool_name

        mcp_tool_schema = adk_to_mcp_tool_type(adk_tool_instance)
        logger.info(
            f"MCP Server: Advertising tool: {mcp_tool_schema.name}, InputSchema: {mcp_tool_schema.inputSchema}"
        )
        mcp_tools_list.append(mcp_tool_schema)
    return mcp_tools_list


@app.call_tool()
async def call_mcp_tool(name: str, arguments: dict) -> list[mcp_types.TextContent]:
    """MCP handler to execute a tool call requested by an MCP client."""
    logger.info(f"MCP Server: Received call_tool request for '{name}' with args: {arguments}")

    if name in ADK_TOOLS:
        adk_tool_instance = ADK_TOOLS[name]
        try:
            adk_tool_response = await adk_tool_instance.run_async(
                args=arguments,
                tool_context=None,  # type: ignore
            )
            logger.info(f"MCP Server: ADK tool '{name}' executed. Response: {adk_tool_response}")
            response_text = json.dumps(adk_tool_response, indent=2)
            return [mcp_types.TextContent(type="text", text=response_text)]

        except Exception as e:
            logger.error(f"MCP Server: Error executing ADK tool '{name}': {e}", exc_info=True)
            error_payload = {
                "success": False,
                "message": f"Failed to execute tool '{name}': {str(e)}",
            }
            error_text = json.dumps(error_payload)
            return [mcp_types.TextContent(type="text", text=error_text)]
    else:
        logger.warning(f"MCP Server: Tool '{name}' not found/exposed by this server.")
        error_payload = {
            "success": False,
            "message": f"Tool '{name}' not implemented by this server.",
        }
        error_text = json.dumps(error_payload)
        return [mcp_types.TextContent(type="text", text=error_text)]


async def run_mcp_stdio_server():
    """Runs the MCP server, listening for connections over standard input/output."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("MCP Stdio Server: Starting handshake with client...")
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
        logger.info("MCP Stdio Server: Run loop finished or client disconnected.")


if __name__ == "__main__":
    logger.info("Launching MCP Server via stdio...")
    try:
        asyncio.run(run_mcp_stdio_server())
    except KeyboardInterrupt:
        logger.info("\nMCP Server (stdio) stopped by user.")
    except Exception as e:
        logger.critical(f"MCP Server (stdio) encountered an unhandled error: {e}", exc_info=True)
    finally:
        logger.info("MCP Server (stdio) process exiting.")
