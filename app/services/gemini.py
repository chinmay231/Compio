import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def summarize_company_profile(about: str, financials: str, news_text: str) -> str:
    prompt = f"""
You are an expert, unbiased finance/business analyst. Use the following three sections to write a detailed company profile.

PART 1 – ABOUT THE COMPANY:
{about}

PART 2 – FINANCIALS:
{financials}

PART 3 – RECENT NEWS ARTICLES:
{news_text}

Write a professional, information-rich summary with:

1. Introduction paragraph
2. In-depth 'Products & Services' section (3-5 sentences)
3. Detailed 'Financial Highlights' section with figures if possible
4. 'Recent Funding or Investment Activity' with named investors, rounds, and years
5. Public Trading status if known and recent news. 

Avoid repetition. Write clearly and do not output templates or placeholders.
"""
    response = model.generate_content(prompt)
    return response.text.strip()
