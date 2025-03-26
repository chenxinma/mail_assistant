import asyncio
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SCRIPT_DIR = Path(__file__).parent

server_params = StdioServerParameters(
    command="uv", # Executable
    args=["run", "src\\mcp_server.py"], # Optional command line arguments
    cwd=str(SCRIPT_DIR.parent), # Optional working directory
)

async def run():
    """run"""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("tools", tools)

            print("session", "fsg_project_assistant call")
            # Call a tool
            result = await session.call_tool("query_documents",
                        arguments={
                            "query_texts": ["项目进展", "基础人事及法定福利服务交付系统"],
                            "n_results": 5,
                            "include": ["metadatas", "documents"]
                        })
            print("result", result)

def test_case01():
    """test_case01"""
    asyncio.run(run())
