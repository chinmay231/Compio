import requests
import os

FMP_API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"

def get_symbol_from_name(company_name):
    url = f"{BASE_URL}/search"
    params = {"query": company_name, "limit": 1, "apikey": FMP_API_KEY}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data[0]["symbol"] if data else None
    except Exception as e:
        print(f"❌ Failed to resolve symbol for {company_name}: {e}")
        return None

def get_fmp_stock_data(symbol):
    url = f"{BASE_URL}/quote/{symbol}?apikey={FMP_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data:
            return "N/A"
        d = data[0]
        return (
            f"- Symbol: {d['symbol']}\n"
            f"- Closing Price Today: ${d['price']}\n"
            f"- P/E Ratio: {d.get('pe', 'N/A')}\n"
            f"- 1-Year Price Growth: {d.get('changesPercentage', 'N/A')}%"
        )
    except Exception as e:
        return f"⚠️ Error retrieving data for {symbol}: {e}"

def get_financial_summary_for_company(company_name):
    symbol = get_symbol_from_name(company_name)
    return get_fmp_stock_data(symbol) if symbol else "Symbol not found"
