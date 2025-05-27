import requests
from bs4 import BeautifulSoup
import time
import random
import urllib.parse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    )
}

def duckduckgo_search(query: str, num_results: int = 5):
    search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
    try:
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if "/l/?" in href and "uddg=" in href:
                parsed = urllib.parse.urlparse(href)
                params = urllib.parse.parse_qs(parsed.query)
                if "uddg" in params:
                    decoded = urllib.parse.unquote(params["uddg"][0])
                    if decoded.startswith("http") and decoded not in links:
                        links.append(decoded)

            if len(links) >= num_results:
                break

        return links
    except Exception as e:
        print(f"❌ DuckDuckGo search failed: {e}")
        return []

def extract_text_from_url(url: str) -> str:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")

        lines = []
        for p in paragraphs:
            try:
                text = p.get_text(strip=True)
                if text:
                    lines.append(text)
            except Exception:
                continue

        return "\n".join(lines)
    except Exception as e:
        print(f"❌ Exception during fetch from {url}: {e}")
        return ""

def search_company_data(company_name: str, num_results: int = 10, min_valid_links: int = 5):
    queries = {
        "about": f"{company_name} company overview",
        "financials": f"{company_name} funding investors revenue"
    }

    results = {}
    for topic, query in queries.items():
        all_links = duckduckgo_search(query, num_results=num_results)
        valid_texts = []
        valid_links = []

        for url in all_links:
            text = extract_text_from_url(url)
            if text.strip():
                valid_texts.append(text)
                valid_links.append(url)
            time.sleep(random.uniform(1.0, 1.5))  # Polite delay

            if len(valid_texts) >= min_valid_links:
                break

        results[topic] = "\n\n---\n\n".join(valid_texts)
        results[f"{topic}_links"] = valid_links

    return results
