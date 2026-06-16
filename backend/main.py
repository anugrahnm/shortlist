from fastapi import HTTPException, FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup
import httpx

class JDInput(BaseModel):
    text: str | None = None
    url: str | None = None

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "OK"}


def fetch_jd_from_url(url):
    response = httpx.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser' )
    text = soup.get_text(strip=True)
    return text

@app.post("/analyze")
def analyze(input: JDInput):
    if input.text:
        return {"message": input.text}
    if input.url:
        try:
            text = fetch_jd_from_url(input.url)
            return {"text": text}
        except httpx.HTTPError as e:
            raise HTTPException(status_code=400, detail="Your request is malformed or invalid")

    else:
        raise HTTPException(status_code=400)