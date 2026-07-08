from mcp.server.fastmcp import FastMCP
import pandas as pd
import os

mcp = FastMCP("Market Price Server")

script_dir = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(script_dir, "prices_trimmed.csv")

CROP_COLUMN_MAP = {
    "beans": "beans", "yam": "yam", "rice": "rice", "millet": "millet",
    "onions": "onions", "milk": "milk", "maize": "maize_fao",
    "beef": "meat_beef", "goat": "meat_goat",
}

EXCLUDED_ADM1 = {"national average", "geopolitical zone", "market average"}

# Lazy-loaded globals — the CSV is NOT read at import time.
# This lets the MCP server respond to the initial handshake instantly,
# instead of blocking on pandas + file I/O before it can even say "I'm ready."
_df = None
_valid_states = None


def normalize_state(raw: str) -> str:
    return raw.lower().replace("state", "").replace("(1)", "").strip()


def _ensure_data_loaded():
    global _df, _valid_states
    if _df is None:
        _df = pd.read_csv(CSV_PATH, parse_dates=["price_date"])
        _valid_states = {
            normalize_state(s) for s in _df["adm1_name"].unique()
            if s.lower() not in EXCLUDED_ADM1
        }


@mcp.tool()
def get_market_price(crop: str, state: str) -> dict:
    """Look up the most recent price for a crop in a given Nigerian state."""
    _ensure_data_loaded()

    col = CROP_COLUMN_MAP.get(crop.lower())
    if col is None:
        return {"error": f"'{crop}' not supported. Try: {', '.join(CROP_COLUMN_MAP)}"}

    norm_state = normalize_state(state)
    if norm_state not in _valid_states:
        return {"error": f"'{state}' not recognized. Valid states: {', '.join(sorted(_valid_states))}"}

    subset = _df[_df["adm1_name"].apply(normalize_state) == norm_state]
    subset = subset[subset[col].notna()]
    if subset.empty:
        return {"error": f"No recent {crop} data for '{state}'"}

    latest_date = subset["price_date"].max()
    latest = subset[subset["price_date"] == latest_date]
    return {
        "crop": crop,
        "state": state,
        "price_ngn": float(round(latest[col].mean(), 2)),
        "as_of": str(latest_date.date()),
        "markets_averaged": int(len(latest)),
    }


if __name__ == "__main__":
    mcp.run()