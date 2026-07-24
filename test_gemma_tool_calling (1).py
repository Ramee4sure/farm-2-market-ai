import os
import re
from google import genai
from google.genai import types

with open(".env") as f:
    content = f.read()
match = re.search(r"GOOGLE_API_KEY\s*=\s*(.+)", content)
key = match.group(1).strip().strip(chr(34))

client = genai.Client(api_key=key)

# Define a simple tool, same shape as your real get_market_price tool
get_market_price_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_market_price",
            description="Get the market price for a crop in a given Nigerian state.",
            parameters={
                "type": "OBJECT",
                "properties": {
                    "crop": {"type": "STRING", "description": "The crop name, e.g. maize"},
                    "state": {"type": "STRING", "description": "The Nigerian state, e.g. Kano"},
                },
                "required": ["crop", "state"],
            },
        )
    ]
)

response = client.models.generate_content(
    model="gemma-4-26b-a4b-it",
    contents="What is the price of maize in Kano?",
    config=types.GenerateContentConfig(tools=[get_market_price_tool]),
)

print("Full response:")
print(response)

print("\n--- Checking for function call ---")
try:
    parts = response.candidates[0].content.parts
    found_call = False
    for part in parts:
        if part.function_call:
            found_call = True
            print("SUCCESS: Model called a function.")
            print("Function name:", part.function_call.name)
            print("Arguments:", dict(part.function_call.args))
        elif part.thought:
            print("(model's internal reasoning, not the answer):")
            print(part.text[:200], "...")
    if not found_call:
        print("NO FUNCTION CALL found in any part — model just returned text instead.")
except Exception as e:
    print("Error inspecting response:", e)
