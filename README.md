# Farm2Market AI

An AI-powered multi-agent system that helps Nigerian farmers make smarter crop-selling decisions using real World Bank food price data.

Built with **Google Agent Development Kit (ADK) 2.0** and **Gemma 4**, for the Build with Gemma AI for Africa Hackathon (Minna 2026).

**Track:** AI for Social Impact

---

## What It Does

A Nigerian farmer can ask in plain language -- "I have 10 bags of maize in Kano, where should I sell?" -- and Farm2Market AI will:

1. Classify whether the query is market-related or unrelated
2. Extract the crop, state, and quantity from the conversation
3. Validate inputs and screen for prompt-injection attempts
4. Look up the real, most recent price from a local dataset backed by World Bank survey data
5. Return personalized selling advice including price context and timing guidance

Every reasoning step (classification, extraction, security screening, advice) is powered by **Gemma 4** (`gemma-4-26b-a4b-it`), accessed via Google's hosted API -- no local GPU required.

---

## Agent Architecture

```
START
  --> classify_and_route
        |--[market_price]--> farmer_input_agent
        |                       --> input_validator (security)
        |                               |--[valid]--> market_data_tool
        |                               |               --> recommendation_agent --> END
        |                               |--[invalid]--> decline_agent --> END
        |--[unrelated]--> decline_agent --> END
```

### Nodes

| Node | Type | Role |
|---|---|---|
| `classify_and_route` | Router + Gemma 4 Agent | Classifies query as `market_price` or `unrelated` |
| `farmer_input_agent` | Gemma 4 Agent | Extracts crop, state, quantity via structured output |
| `input_validator` | Gemma 4 Agent + Programmatic | Validates crop/state; screens for prompt injection |
| `market_data_tool` | **Deterministic function node (no LLM)** | Directly calls `get_market_price(crop, state)` -- see design note below |
| `recommendation_agent` | Gemma 4 Agent | Generates personalized selling advice |
| `decline_agent` | Gemma 4 Agent | Politely declines unrelated or invalid queries, naming the specific issue |

### Design note: why `market_data_tool` isn't an LLM

Early versions routed this step through an LLM-driven tool call. During testing, this occasionally failed silently (a connection timing issue), and the downstream recommendation agent -- receiving no real data -- fabricated a plausible-sounding but entirely invented price and date. Since a price lookup requires no judgment, this step was rebuilt as a plain deterministic function call. This removes the entire failure class: there is no model in the loop that could choose not to call the function, or misreport what it returned. The `recommendation_agent` also has an explicit instruction to never invent data under any circumstance, as a second layer of protection.

---

## Data Source

**World Bank: Monthly Food Price Estimates by Product and Market**
- Nigeria, 73 markets, January 2007 - May 2026
- Reference ID: NGA_2021_RTFP_v02_M
- License: Creative Commons Attribution 4.0 (CC BY 4.0)
- Citation: Andree, B.P.J. (2021). *Monthly food price estimates by product and market* (Version 2026-05-18). Washington, DC: World Bank Microdata Library.

**Supported crops:** beans, yam, rice, millet, onions, milk, maize, beef, goat

**Supported states:** Abia, Adamawa, Borno, Gombe, Jigawa, Kaduna, Kano, Katsina, Kebbi, Lagos, Oyo, Sokoto, Yobe, Zamfara

> Note: Prices are estimates from the latest available monthly survey data, not a live feed. Verified real example: maize in Kano State, NGN 390, as of March 2026, averaged from 1 market.

---

## Project Structure

This repository's root **is** the agent project -- there is no extra subfolder to `cd` into.

```
farm-2-market-ai/            (this repo, after cloning)
|-- agent.py                 # Full ADK 2.0 workflow -- all nodes, edges
|-- __init__.py               # Exposes root_agent
|-- .env                      # API key config (you create this -- see setup below)
|-- test_agent.py             # Scenario test suite
|-- validate_agent.py         # Graph compilation validator
`-- mcp_server/
    |-- market_server.py       # get_market_price lookup function
    `-- prices_trimmed.csv     # Trimmed World Bank dataset (2024-2026)
```

---

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- A Gemini API key from [Google AI Studio](https://aistudio.google.com) (this same key is used to access Gemma 4 -- no separate key needed)

### 1. Clone the repo

```bash
git clone https://github.com/Ramee4sure/farm-2-market-ai.git
cd farm-2-market-ai
```

### 2. Install agents-cli

```bash
uvx google-agents-cli setup
```

### 3. Create and activate a virtual environment (inside this repo folder)

```bash
python -m venv venv

# Windows
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure your API key

Create a file named `.env` in the root of this repo (same folder as `agent.py`):

```
GOOGLE_API_KEY=your_gemini_api_key_here
GOOGLE_GENAI_USE_ENTERPRISE=FALSE
```

> Get a free key at https://aistudio.google.com. This key is used to access Gemma 4 (`gemma-4-26b-a4b-it`) via Google's hosted API -- the same endpoint used for Gemini.

### 6. Run the agent

Single query:
```bash
# Windows (from the repo root, one level above this folder)
cd ..
venv\Scripts\adk run farm-2-market-ai "I have 10 bags of maize in Kano, what price should I expect?"

# macOS/Linux
cd ..
venv/bin/adk run farm-2-market-ai "I have 10 bags of maize in Kano, what price should I expect?"
```

> Note: `adk run` expects the agent folder name as an argument from its *parent* directory -- run it from one level above this repo, not from inside it.

Interactive mode (multi-turn conversation):
```bash
adk run farm-2-market-ai
```

### 7. Run the test suite

```bash
# from inside the repo folder
python test_agent.py
```

---

## Known Limitations

- Price data covers 14 Nigerian states only (based on World Bank survey coverage)
- Most recent price data is from early 2026 -- not a live feed
- Gemma 4's free tier has a daily request limit; heavy repeated testing may exhaust it (each scenario uses several requests across the multiple agents in the pipeline)

---

## Author

**Ramadan** ([@Ramee4sure](https://github.com/Ramee4sure))

Built solo for the Build with Gemma AI for Africa Hackathon, GDG on Campus Federal University of Technology Minna, 2026.
