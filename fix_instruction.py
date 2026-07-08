with open("agent.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """instruction=(
        "You are a market database access assistant. "
        "Your task is to fetch the price of the crop in the given state. "
        "You must call the get_market_price tool with the exact crop and state names. "
        "Do not answer the user directly. Just output the result of the tool call exactly as it is returned."
    ),"""

new = """instruction=(
        "You are a market database access assistant. "
        "Your task is to fetch the price of the crop in the given state. "
        "You must call the get_market_price tool with the exact crop and state names. "
        "After receiving the tool result, you MUST output a final text response "
        "containing the exact JSON result of the tool call. Always produce text output, "
        "never end your turn without writing out the tool result as text."
    ),"""

if old not in content:
    print("WARNING: exact block not found, no changes made.")
else:
    content = content.replace(old, new)
    with open("agent.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched successfully.")
