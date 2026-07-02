# Farm2Market AI 🌾

An AI-powered multi-agent system that helps Nigerian farmers make smarter crop-selling decisions using real World Bank food price data.

Built with **Google Agent Development Kit (ADK) 2.0** as a capstone project for the Kaggle 5-Day AI Agents Intensive Vibe Coding Course with Google.

**Track:** Agents for Good

---

## What It Does

A Nigerian farmer can ask in plain language — "I have 10 bags of maize in Kano, where should I sell?" — and Farm2Market AI will:

1. Classify whether the query is market-related or unrelated
2. Extract the crop, state, and quantity from the conversation
3. Validate inputs and screen for prompt-injection attempts
4. Look up real, recent price data via a local MCP server backed by World Bank data
5. Return personalized selling advice including price context and timing guidance

---

## Agent Architecture

```
START
  └─► classify_and_route
        ├─[market_price]─► farmer_input_agent
        │                       └─► input_validator (security)
        │                               ├─[valid]─► market_data_tool (MCP)
        │                               │               └─► recommendation_agent ─► END
        │                               └─[invalid]─► decline_agent ─► END
        └─[unrelated]──► decline_agent ─► END
```

### Nodes

| Node | Type | Role |
|---|---|---|
| `classify_and_route` | Router + LLM Agent | Classifies query as `market_price` or `unrelated` |
| `farmer_input_agent` | LLM Agent | Extracts crop, state, quantity via structured output |
| `input_validator` | LLM Agent + Programmatic | Validates crop/state; screens for prompt injection |
| `market_data_tool` | LLM Agent + MCP | Calls `get_market_price(crop, state)` via MCP server |
| `recommendation_agent` | LLM Agent | Generates personalized selling advice |
| `decline_agent` | LLM Agent | Politely declines unrelated or invalid queries |

### Course Concepts Demonstrated

- **Multi-agent orchestration** — 5-node ADK 2.0 graph workflow with conditional routing
- **MCP server integration** — `mcp_server/market_server.py` exposes `get_market_price` tool via stdio transport
- **Security/validation layer** — `input_validator` checks crop/state validity and screens for prompt-injection patterns

---

## Data Source

**World Bank: Monthly Food Price Estimates by Product and Market**
- Nigeria, 73 markets, January 2007 – May 2026
- Reference ID: NGA_2021_RTFP_v02_M
- License: Creative Commons Attribution 4.0 (CC BY 4.0)
- Citation: Andrée, B.P.J. (2021). *Monthly food price estimates by product and market* (Version 2026-05-18). Washington, DC: World Bank Microdata Library.

**Supported crops:** beans, yam, rice, millet, onions, milk, maize, beef, goat

**Supported states:** Abia, Adamawa, Borno, Gombe, Jigawa, Kaduna, Kano, Katsina, Kebbi, Lagos, Oyo, Sokoto, Yobe, Zamfara

> Note: Prices are estimates from the latest available monthly survey data, not live market feeds. Data is grounded in real World Bank price surveys.

---

## Project Structure

```
farm2market_agent/
├── agent.py              # Full ADK 2.0 workflow — all nodes, edges, MCP connection
├── __init__.py           # Exposes root_agent
├── .env                  # API key config (not committed — see setup below)
├── test_agent.py         # 4-scenario test suite
├── validate_agent.py     # Graph compilation validator
└── mcp_server/
    ├── market_server.py  # FastMCP server exposing get_market_price tool
    └── prices_trimmed.csv # Trimmed World Bank dataset (2024–2026)
```

---

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+
- A Gemini API key from [Google AI Studio](https://aistudio.google.com)

### 1. Clone the repo

```bash
git clone https://github.com/Ramee4sure/farm2market-ai.git
cd farm2market-ai
```

### 2. Install agents-cli

```bash
uvx google-agents-cli setup
```

### 3. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install google-adk fastmcp pandas
```

### 5. Configure your API key

Create a `.env` file inside `farm2market_agent/`:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

> Get a free key at https://aistudio.google.com — the project uses `gemini-2.0-flash` by default.

### 6. Download the World Bank dataset

The trimmed dataset (`prices_trimmed.csv`) is included in this repo. If you want to regenerate it from the full source:

1. Download `NGA_RTFP_mkt_2007_2026-05-18.csv` from the [World Bank Microdata Library](https://microdata.worldbank.org/catalog/4503/get-microdata) (free account required)
2. Place it in `farm2market_agent/mcp_server/`
3. Run: `python trim_data.py` from inside `farm2market_agent/`

### 7. Run the agent

Single query:
```bash
# Windows
cd farm2market_agent
..\venv\Scripts\adk run farm2market_agent "I have 10 bags of maize in Kano, what price should I expect?"

# macOS/Linux
adk run farm2market_agent "I have 10 bags of maize in Kano, what price should I expect?"
```

Interactive mode (multi-turn conversation):
```bash
adk run farm2market_agent
```

### 8. Run the test suite

```bash
cd farm2market_agent
..\venv\Scripts\python.exe test_agent.py   # Windows
python test_agent.py                        # macOS/Linux
```

---

## Known Limitations

- Price data covers 14 Nigerian states only (based on World Bank survey coverage)
- Most recent price data is from early 2026 — not a live feed
- `gemini-2.0-flash` free tier has a daily request limit (1,500 requests/day); heavy testing may exhaust it

---

## Author

**Ramadan** ([@Ramee4sure](https://github.com/Ramee4sure))

Built solo for the Kaggle 5-Day AI Agents Intensive Vibe Coding Course with Google, July 2026
