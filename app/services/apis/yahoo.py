import requests
import re
import json

def search_yahoo_finance(query: str, max_results: int = 5):
    """Search Yahoo Finance for matching companies and return suggestions."""
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount={max_results}&newsCount=0"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        results = response.json().get("quotes", [])
        return [
            {
                "name": r["shortname"],
                "symbol": r["symbol"],
                "exchange": r.get("exchange", "N/A")
            }
            for r in results if "symbol" in r and "shortname" in r
        ]
    except Exception as e:
        print(f"Yahoo Finance Search Error: {e}")
        return []

def get_yahoo_financials(symbol: str):
    """
    Fetches Current Price and Market Cap from Yahoo Finance using embedded JSON (no Selenium).
    """
    url = f"https://finance.yahoo.com/quote/{symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Extract JSON data
        match = re.search(r'root\.App\.main\s*=\s*(\{.*?\});\n', response.text)
        if not match:
            print(f"⚠️ Failed to parse Yahoo JSON for {symbol}")
            return {
                "symbol": symbol,
                "current_price": "N/A",
                "market_cap": "N/A"
            }

        data = json.loads(match.group(1))
        store = data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]
        price = store.get("price", {}).get("regularMarketPrice", {}).get("raw", None)
        market_cap = store.get("summaryDetail", {}).get("marketCap", {}).get("fmt", None)

        return {
            "symbol": symbol,
            "current_price": f"${price}" if price else "N/A",
            "market_cap": market_cap if market_cap else "N/A"
        }

    except Exception as e:
        print(f"❌ Yahoo scrape failed for {symbol}: {e}")
        return {
            "symbol": symbol,
            "current_price": "N/A",
            "market_cap": "N/A"
        }
