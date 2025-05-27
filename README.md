# 📊 Compio: Company Insight Generator

Compio is a lightweight web-based tool that generates summarized company profiles, compiles financial and funding data, fetches relevant recent news, and exports everything into structured `.docx` files. The project is designed using AWS S3, BS4 web-scraping, FastAPI, Google Gemini, and Yahoo Finance scraping to give a complete view of a business from real-time internet sources.

---

## 🚀 Features

- 🔍 Real-time company lookup with dropdown autocomplete from Yahoo Finance
- 📄 Summarized company profile generated using Google Gemini
- 📈 Financials and funding info extracted via scraping and APIs
- 📰 Recent news fetched and summarized from Google News
- 💾 Raw and source-linked `.docx` files stored on AWS S3
- 🖥️ Simple frontend for usage

---

## 🧱 Folder Structure

```bash
compio/
├── app/
│   ├── main.py               # FastAPI app instance
│   ├── routes/
│   │   ├── generate.py       # API endpoint: /api/generate
│   │   └── enlighten.py      # API endpoint: /api/enlighten (autocomplete)
│   ├── services/
│   │   ├── gemini.py         # Gemini API integration
│   │   ├── s3_upload.py      # AWS S3 uploader
│   │   ├── docx_writer.py    # Writers for .docx output
│   │   │── scraper/
│   │   │   ├── webscrape.py     # DuckDuckGo scraper for text content
│   │   │   ├── newsscrape.py    # Google News scraper and summarizer
│   │   └── apis/
│   │       └── fmp.py           #Optional API Calls for Financial Data Ingestion
│   │       └── twelve_data.py   #Optional API Calls for Financial Data Ingestion
│   │       └── yahoo.py         # Yahoo Finance autocomplete and ticker lookup
├── frontend/
│   └── index.html            # Basic frontend interface
├── .env                      # API keys and secrets (Access the file called extra. env and rename it .env)
├── requirements.txt          # Python dependencies
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/chinmay231/compio
cd compio
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File
Add the following to your `.env`:
```env
GOOGLE_API_KEY=your_google_gemini_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-west-2
S3_BUCKET_NAME=compio-docs-chinmay
```

### 5. Run the Application
```bash
uvicorn app.main:app --reload
```
Then open your browser to: [http://localhost:8000](http://localhost:8000)

---

## 📌 API Endpoints

### `/api/enlighten?company=Tesla`
Returns top matching company names from Yahoo Finance autocomplete.

### `/api/generate?company=Tesla Inc`
- Fetches about + financial info using DuckDuckGo
- Extracts news articles
- Summarizes everything with Gemini
- Uploads `.docx` to S3
- Returns compiled summary and link references

---

## 🔐 Environment Variables Summary
.env file

---

## 📄 requirements.txt
```
fastapi
uvicorn[standard]
python-docx
requests
beautifulsoup4
boto3
google-generativeai
python-dotenv
```

---

## 📣 Contributions & Extensions
If you’d like to:
- Add LLM-based comparisons with other modules
- Support via Crunchbase/Octoparse for data ingestion
- Improve UI or visualization by adding financial data and graphs 

Feel free to fork and contribute. PRs welcome!

---

## 🧠 Credits
Created by Chinmay Kapoor, with as a practice to enable AWS S3, APIs for data ingestion and multi-source data compilation using Gemini API.

---

## 📬 Contact
[LinkedIn]((https://www.linkedin.com/in/chinmay-kapoor-b67344200/)) | [Email](mailto:chinmaykapoor2301@gmail.com)
