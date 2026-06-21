# Shortlist

Match your CV to any job description in seconds.

Live at: [shortlist.anugrah.dev](https://shortlist.anugrah.dev)

## What it does

Paste a job description (or a URL) and Shortlist compares it against your CV and returns:

- A match score
- Keywords you already cover
- Keywords missing from your CV
- A brief review of your fit for the role (AI mode only)

## Modes

**AI mode (Gemini)** uses Google Gemini 3.1 Flash Lite to analyse the JD against your CV. It can scrape URLs directly, handles JS-rendered pages, and understands context and synonyms. This is the recommended mode.

**TF-IDF mode** uses pure NLP with no API calls. It vectorises both documents and computes cosine similarity to produce a match score. It is fast and free but only matches exact words. It will not catch synonyms, context, or skills mentioned under different phrasing. Use this mode with pasted text for best results, and treat the output as a rough indicator rather than an accurate assessment.

## Stack

- **Frontend** Vue 3, Vite, TypeScript, Tailwind CSS
- **Backend** FastAPI, Python
- **Matching** scikit-learn (TF-IDF + cosine similarity), Google Gemini API
- **Scraping** httpx, BeautifulSoup4
- **Hosting** DigitalOcean VPS, Caddy, Docker, GitHub Actions CI/CD

## Running locally

**Backend**

```bash
cd backend
uv sync
cp .env.example .env  # add your GEMINI_API_KEY
uv run uvicorn main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
cp .env.example .env.development  # set VITE_API_URL=http://localhost:8000
npm run dev
```

## Notes

- Results are cached in the browser for the session. Submitting the same JD again in the same mode will return the cached result instantly without hitting the API.
- URL scraping works best with plain HTML pages. JS-heavy sites like LinkedIn may not parse correctly in TF-IDF mode. Use AI mode or paste the text instead.
- The CV is stored as a static text file at `backend/cv.txt`. Update it with your own CV to use the tool.
