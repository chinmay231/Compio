from pathlib import Path
import re
from fastapi import APIRouter, Query

from app.services.scraper.webscrape import search_company_data
from app.services.gemini import summarize_company_profile
from app.services.docx_writer import write_meta_raw_docx, write_meta_links_docx
from app.services.s3_upload import upload_to_s3
from app.services.apis.yahoo import search_yahoo_finance
from app.services.scraper.newsscrape import get_news_snippets, extract_text_from_news_links

router = APIRouter()

def safe_filename(company: str) -> str:
    return re.sub(r'[^\w\-_\. ]', '_', company.strip().replace(" ", "_"))

@router.get("/generate")
async def generate(company: str = Query(...)):
    # Step 1: Scrape company data from DuckDuckGo
    results = search_company_data(company)

    # Step 2: Get news markdown and URLs
    news_links_markdown, news_urls = get_news_snippets(company, return_links=True)
    news_text = extract_text_from_news_links(news_urls)

    # Step 3: Summarize all content using Gemini
    summary = summarize_company_profile(results["about"], results["financials"], news_text)

    # Step 4: Add ticker symbol info
    symbol_data = search_yahoo_finance(company)
    if symbol_data:
        ticker = symbol_data[0]["symbol"]
        exchange = symbol_data[0].get("exchange", "N/A")
        summary += f"\n\n🔎 Matched Symbol: {ticker} ({exchange})"
    else:
        summary += f"\n\n🔎 Symbol not found on Yahoo Finance."

    # Step 5: Append latest news in markdown format
    if news_links_markdown:
        summary += f"\n\n📰 Recent News:\n{news_links_markdown}"

    # Step 6: Write documents
    safe_name = safe_filename(company)
    raw_file = f"{safe_name}_raw.docx"
    link_file = f"{safe_name}_links.docx"

    write_meta_raw_docx(results["about"], results["financials"], raw_file)
    write_meta_links_docx(results["about_links"], results["financials_links"], news_urls, link_file)

    # Step 7: Upload to S3
    upload_to_s3(raw_file, f"{company}/{Path(raw_file).name}")
    upload_to_s3(link_file, f"{company}/{Path(link_file).name}")

    # Step 8: Return final payload
    return {
        "company": company,
        "compiled_summary": summary,
        "links_used": {
            "about_links": results["about_links"],
            "financials_links": results["financials_links"],
            "news_links": news_urls
        },
        "s3_knowledge_base": {
            "raw_doc": f"s3://compio-docs-chinmay/{company}/{Path(raw_file).name}",
            "link_doc": f"s3://compio-docs-chinmay/{company}/{Path(link_file).name}"
        }
    }
