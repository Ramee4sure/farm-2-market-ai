with open("agent.py", "r", encoding="utf-8") as f:
    content = f.read()

changes_made = []

old_market_tool = """instruction=(
        "You are a market database access assistant. "
        "Your task is to fetch the price of the crop in the given state. "
        "You must call the get_market_price tool with the exact crop and state names. "
        "After receiving the tool result, you MUST output a final text response "
        "containing the exact JSON result of the tool call. Always produce text output, "
        "never end your turn without writing out the tool result as text."
    ),"""

new_market_tool = """instruction=(
        "You are a market database access assistant. "
        "You have access to a real function called get_market_price. You MUST invoke it "
        "using your function-calling capability -- do not write out a JSON description of "
        "the function call as plain text, and do not simulate or guess what it would return. "
        "Actually call the function using the tool-calling mechanism available to you. "
        "Only after the function has actually executed and returned a real result, "
        "output that real result as text, exactly as returned, with no invented values."
    ),"""

if old_market_tool in content:
    content = content.replace(old_market_tool, new_market_tool)
    changes_made.append("market_data_tool instruction updated")
else:
    print("WARNING: market_data_tool instruction block not found -- no change made there.")

import re
pattern = r"(def get_recommendation_instruction\(ctx: ReadonlyContext\) -> str:.*?return \()"
match = re.search(pattern, content, re.DOTALL)
if match:
    insertion = (
        "\n        \"CRITICAL RULE: You will be given tool output data. If that data is missing, "
        "malformed, contains an error field, or is not an actual price result (for example, if it "
        "looks like a function call description rather than real returned data), you MUST NOT invent, "
        "guess, or assume any price, date, or market count. Instead, respond honestly: tell the farmer "
        "you were unable to retrieve current price data and ask them to try again. Never fabricate "
        "numbers under any circumstance, even to demonstrate formatting. \"\n        "
    )
    content = content[:match.end()] + insertion + content[match.end():]
    changes_made.append("recommendation_agent anti-fabrication rule inserted")
else:
    print("WARNING: could not find recommendation instruction return statement -- no change made there.")

with open("agent.py", "w", encoding="utf-8") as f:
    f.write(content)

if changes_made:
    print("Applied fixes:")
    for c in changes_made:
        print(" -", c)
else:
    print("No changes were applied. Manual inspection needed.")
