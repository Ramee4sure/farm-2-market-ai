import re

with open("agent.py", "r", encoding="utf-8") as f:
    content = f.read()

old_block = """# Locate market_server.py dynamically
if os.path.exists(os.path.join(farm2market_dir, "mcp_server", "market_server.py")):
    mcp_cwd = farm2market_dir
    mcp_args = ["mcp_server/market_server.py"]
elif os.path.exists(os.path.join(parent_dir, "mcp_server", "market_server.py")):
    mcp_cwd = parent_dir
    mcp_args = ["mcp_server/market_server.py"]
else:
    mcp_cwd = os.getcwd()
    mcp_args = ["mcp_server/market_server.py"]"""

new_block = """# Locate market_server.py dynamically
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
    mcp_args = ["market_server.py"]"""

if old_block not in content:
    print("WARNING: exact block not found, no changes made. Manual check needed.")
else:
    content = content.replace(old_block, new_block)
    with open("agent.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched successfully.")
