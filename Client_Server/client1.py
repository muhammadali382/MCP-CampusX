import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage
import json

load_dotenv()

SERVERS = { 
    "math": {
        "transport": "stdio",
        "command": "/home/aiml/.local/bin/uv",
        "args": [
            "run",
            "fastmcp",
            "run",
            "/home/aiml/Documents/Projects/Learn-FastMCP/Client_Server/main1.py"
       ]
    },
    # "expense": {
    #     "transport": "http",  # if this fails, try "sse"
    #     "url": "https://deploy-test.fastmcp.app/mcp"
    # },
    "manim-server": {
        "transport": "stdio",
        "command": "/home/aiml/Documents/Projects/Learn-FastMCP/.venv/bin/python",
        "args": [
        "/home/aiml/Documents/Projects/MCP/manim-mcp-server/src/manim_server.py"
        ],
        "env": {
            "MANIM_EXECUTABLE": "/home/aiml/.local/bin/manim",
       
        }
    }
}

async def main():
    
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()


    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    print("Available tools:", named_tools.keys())

    llm = ChatGroq(
        model="qwen/qwen3.6-27b",
        temperature=0
    )
    llm_with_tools = llm.bind_tools(tools)

    prompt = "draw a triangle rotating in place using manim tool."
    response = await llm_with_tools.ainvoke(prompt)

    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return

    tool_messages = []
    for tc in response.tool_calls:
        selected_tool = tc["name"]
        selected_tool_args = tc.get("args") or {}
        selected_tool_id = tc["id"]

        result = await named_tools[selected_tool].ainvoke(selected_tool_args)
        tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
        

    final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
    print(f"Final response: {final_response.content}")


if __name__ == '__main__':
    asyncio.run(main())