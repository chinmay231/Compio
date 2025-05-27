import requests
from bs4 import BeautifulSoup
import time
import random

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    )
}

def get_news_snippets(company_name: str, max_articles: int = 5, return_links: bool = False):
    """
    Fetches recent news headlines from Google News for a given company.
    Returns markdown-style bullet points and optionally the raw URLs.
    """
    url = f"https://news.google.com/search?q={company_name.replace(' ', '%20')}&hl=en-US&gl=US&ceid=US:en"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all("article")[:max_articles]
        markdown_news = []
        links = []

        for article in articles:
            a_tag = article.find("a", href=True)
            title_tag = a_tag.find("span") if a_tag else None
            if a_tag and title_tag:
                title = title_tag.get_text(strip=True)
                href = a_tag["href"]
                link = f"https://news.google.com{href[1:]}" if href.startswith(".") else href
                markdown_news.append(f"- [{title}]({link})")
                links.append(link)

        if return_links:
            return "\n".join(markdown_news), links
        return "\n".join(markdown_news) if markdown_news else "No relevant news found."

    except Exception as e:
        print(f"News scraping failed: {e}")
        return ("News could not be retrieved at this time.", []) if return_links else "News could not be retrieved at this time."

def extract_text_from_news_links(news_urls, max_articles=5):
    """
    Extracts full article text (plain paragraphs) from a list of news URLs.
    Combines the content of up to max_articles into one string.
    """
    combined_text = []

    for url in news_urls[:max_articles]:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            paragraphs = soup.find_all("p")
            text = " ".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            if text:
                combined_text.append(text)

            time.sleep(random.uniform(1.0, 2.0))  # polite delay
        except Exception as e:
            print(f"❌ Failed to fetch article from {url}: {e}")

    return "\n\n---\n\n".join(combined_text) if combined_text else "No news article text could be extracted."
