with open("agent.py", "r", encoding="utf-8") as f:
    content = f.read()

old_section = '''# 6. MCP Server Connection & Market Data Tool Agent
current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
parent_dir = os.path.dirname(current_dir)
farm2market_dir = os.path.join(parent_dir, "farm2market")

# Locate market_server.py dynamically
if os.path.exists(os.path.join(current_dir, "mcp_server", "market_server.py")):
    mcp_cwd = os.path.join(current_dir, "mcp_server")
    mcp_args = ["market_server.py"]
elif os.path.exists(os.path.join(farm2market_dir, "mcp_server", "market_server.py")):
    mcp_cwd = os.path.join(farm2market_dir, "mcp_server")
    mcp_args = ["market_server.py"]
elif os.path.exists(os.path.join(parent_dir, "mcp_server", "market_server.py")):
    mcp_cwd = os.path.join(parent_dir, "mcp_server")
    mcp_args = ["market_server.py"]
else:
    mcp_cwd = os.path.join(os.getcwd(), "mcp_server")
    mcp_args = ["market_server.py"]

# Resolve the python executable of the virtual environment to ensure libraries like fastmcp are available
venv_python = os.path.join(parent_dir, "venv", "Scripts", "python.exe")
if not os.path.exists(venv_python):
    venv_python = os.path.join(parent_dir, "venv", "bin", "python")
if not os.path.exists(venv_python):
    venv_python = "python"

mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=venv_python,
            args=mcp_args,
            cwd=mcp_cwd,
        )
    )
)

market_data_tool = Agent(
    model='gemma-4-26b-a4b-it',
    name='market_data_tool',
    instruction=(
        "You are a market database access assistant. "
        "You have access to a real function called get_market_price. You MUST invoke it "
        "using your function-calling capability -- do not write out a JSON description of "
        "the function call as plain text, and do not simulate or guess what it would return. "
        "Actually call the function using the tool-calling mechanism available to you. "
        "Only after the function has actually executed and returned a real result, "
        "output that real result as text, exactly as returned, with no invented values."
    ),
    tools=[mcp_toolset],
    include_contents='none',
)'''

new_section = '''# 6. Market Data Node -- deterministic function call, no LLM involved.
# This lookup is a pure data operation with no judgment required, so it runs as
# a plain node instead of an LLM agent. This removes the MCP-session-timing race
# condition and the risk of a model narrating a tool call instead of making one.
import sys
import json

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
parent_dir = os.path.dirname(current_dir)
farm2market_dir = os.path.join(parent_dir, "farm2market")

if os.path.exists(os.path.join(current_dir, "mcp_server", "market_server.py")):
    mcp_server_dir = os.path.join(current_dir, "mcp_server")
elif os.path.exists(os.path.join(farm2market_dir, "mcp_server", "market_server.py")):
    mcp_server_dir = os.path.join(farm2market_dir, "mcp_server")
elif os.path.exists(os.path.join(parent_dir, "mcp_server", "market_server.py")):
    mcp_server_dir = os.path.join(parent_dir, "mcp_server")
else:
    mcp_server_dir = os.path.join(os.getcwd(), "mcp_server")

if mcp_server_dir not in sys.path:
    sys.path.insert(0, mcp_server_dir)

from market_server import get_market_price as _get_market_price_fn


@node(rerun_on_resume=True)
async def market_data_tool(ctx: Context, node_input: Any) -> Event:
    crop = ctx.state.get("crop", "")
    state = ctx.state.get("state", "")
    result = _get_market_price_fn(crop=crop, state=state)
    return Event(output=json.dumps(result))'''

if old_section in content:
    content = content.replace(old_section, new_section)
    with open("agent.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced market_data_tool with a deterministic function node. Success.")
else:
    print("WARNING: exact section not found -- no changes made. Manual inspection needed.")
