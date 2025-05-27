import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TWELVE_DATA_API_KEY")

BASE_URL = "https://api.twelvedata.com"

def get_quote(ticker: str):
    url = f"{BASE_URL}/quote?symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_price_1y_change(ticker: str):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=365)
    
    url = (
        f"{BASE_URL}/time_series?symbol={ticker}"
        f"&interval=1day&start_date={start_date}&end_date={end_date}&apikey={API_KEY}"
    )
    
    response = requests.get(url).json()
    values = response.get("values", [])
    
    if len(values) < 2:
        return None, None, None
    
    latest = float(values[0]['close'])
    oldest = float(values[-1]['close'])
    percent_change = ((latest - oldest) / oldest) * 100
    
    return latest, oldest, round(percent_change, 2)

def get_financial_summary(ticker: str) -> str:
    quote = get_quote(ticker)
    today_close, year_ago_close, year_growth = get_price_1y_change(ticker)
    
    if "code" in quote:
        return f"⚠️ Error retrieving data for {ticker}: {quote.get('message', '')}"
    
    summary_lines = []

    summary_lines.append(f"📈 **{quote['name']} ({ticker}) Financial Snapshot**")
    summary_lines.append(f"- Market Cap: ${quote.get('market_cap', 'N/A')}")
    summary_lines.append(f"- P/E Ratio: {quote.get('pe', 'N/A')}")
    summary_lines.append(f"- Today's Open: ${quote.get('open', 'N/A')}")
    summary_lines.append(f"- Today's Close: ${quote.get('close', 'N/A')}")

    if year_growth is not None:
        summary_lines.append(f"- 1-Year Price Growth: {year_growth}%")
    else:
        summary_lines.append("- 1-Year Price Growth: N/A")

    return "\n".join(summary_lines)
