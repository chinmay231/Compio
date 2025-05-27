from app.services.scraper.webscrape import search_company_data
from app.services.docx_writer import write_meta_raw_docx, write_meta_links_docx, write_compiled_docx
from app.services.s3_upload import upload_to_s3
from app.services.gemini import summarize_company_profile
from pathlib import Path
import re

def safe_filename(company: str) -> str:
    return re.sub(r'[^\w\-_\. ]', '_', company.strip().replace(" ", "_"))

company = "Meta Platforms Inc"
print(f"🔍 Fetching data for: {company}")

results = search_company_data(company)

safe_name = safe_filename(company)
raw_file = f"{safe_name}_raw.docx"
link_file = f"{safe_name}_links.docx"
compiled_file = f"{safe_name}_compiled.docx"

write_meta_raw_docx(results["about"], results["financials"], raw_file)
write_meta_links_docx(results["about_links"], results["financials_links"], link_file)

summary = summarize_company_profile(results["about"], results["financials"])
write_compiled_docx(summary, compiled_file)

upload_to_s3(raw_file, f"{company}/{Path(raw_file).name}")
upload_to_s3(link_file, f"{company}/{Path(link_file).name}")
upload_to_s3(compiled_file, f"{company}/{Path(compiled_file).name}")

print("✅ All files created and uploaded.")

print("\n🧠 Compiled Company Summary:\n")
print(summary)

print("\n🔗 Links Used:\n")
print("• About Links:")
for link in results["about_links"]:
    print("  -", link)

print("\n• Financials Links:")
for link in results["financials_links"]:
    print("  -", link)
