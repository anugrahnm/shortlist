from fastapi import HTTPException, FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import httpx
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

from google import genai

client = genai.Client()

def gemini(cv, jd):
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=f"""My CV:{cv} and the JD:{jd}"""
    )
    return response.text


class JDInput(BaseModel):
    text: str | None = None
    url: str | None = None

app = FastAPI()

origins = [
    "http://localhost:5173" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"]
)

vectorizer = TfidfVectorizer(stop_words="english", lowercase=True)

@app.get("/health")
def health_check():
    return {"status": "OK"}

with open("cv.txt", "r") as f:
    cv = f.read()


def fetch_jd_from_url(url):
    response = httpx.get(url)
    html_content = response.text
    print(html_content)
    soup = BeautifulSoup(html_content, 'html.parser' )
    element = soup.find('div', attrs={'data-testid':'job-card-main'})
    text_content = element.get_text(strip=True)
    return text_content

def calculate_match(cv_text, jd_text):
    vectors = vectorizer.fit_transform([cv_text, jd_text])
    feature_names = vectorizer.get_feature_names_out()
    vectors_jd = vectors[1].toarray().flatten()
    jd_keywords = list(zip(feature_names, vectors_jd))
    jd_keywords.sort(key=lambda x: x[1], reverse=True)

    matched = [jd_keyword for jd_keyword in jd_keywords if jd_keyword[0] in cv_text.lower() and jd_keyword[1] > 0]

    missing = [jd_keyword for jd_keyword in jd_keywords if jd_keyword[0] not in cv_text.lower() and jd_keyword[1] > 0]

    cos_sim = cosine_similarity(vectors)
    return {"matched": matched, "missing": missing, "score":cos_sim[0,1]}


@app.post("/analyze/")
def analyze(input: JDInput):
    if input.text:
        score = calculate_match(cv, input.text)
        return {"matched":score["matched"],"missing":score["missing"],"score": score["score"]}
    if input.url:
        try:
            text = fetch_jd_from_url(input.url)
            score = calculate_match(cv, text)
            return {"matched":score["matched"],"missing":score["missing"],"score": score["score"]}
        except httpx.HTTPError as e:
            raise HTTPException(status_code=400, detail="Your request is malformed or invalid")
    else:
        raise HTTPException(status_code=400)

@app.post("/analyze/gemini/")
def gemini_analyze(input:JDInput):
    if input.text:
        score = gemini(cv, input.text)
        return {"matched":score["matched"],"missing":score["missing"],"score": score["score"]}
    if input.url:
        try:
            text = fetch_jd_from_url(input.url)
            score = gemini(cv, text)
            return {"matched":score["matched"],"missing":score["missing"],"score": score["score"]}
        except httpx.HTTPError as e:
            raise HTTPException(status_code=400, detail="Your request is malformed or invalid")
    else:
        raise HTTPException(status_code=400)