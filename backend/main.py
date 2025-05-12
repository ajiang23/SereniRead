import os
import json
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

logging.basicConfig(level=logging.INFO)

GOOGLE_KEY = os.getenv("GOOGLE_KEY")

static_dir = Path(__file__).parent / "static"
TRIGGERS = json.loads((static_dir / "triggers.json").read_text())
THEMES   = json.loads((static_dir / "themes.json").read_text())

def keyword_classify(text: str, candidates: list[str]) -> list[str]:
    t = text.lower()
    picks = [c for c in candidates if c.lower() in t]
    return picks if picks else candidates[:3]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

@app.get("/search")
async def search(q: str = Query(..., min_length=1)):
    params = {"q": q, "maxResults": 10, "key": GOOGLE_KEY}
    async with httpx.AsyncClient() as http:
        resp = await http.get("https://www.googleapis.com/books/v1/volumes", params=params)
        data = resp.json()

    if "error" in data:
        raise HTTPException(status_code=502, detail=data["error"].get("message"))
    items = data.get("items", [])

    results = []
    for item in items:
        info = item.get("volumeInfo", {})
        bid = item.get("id", "")
        title = info.get("title", "Unknown Title")
        desc  = info.get("description", "")

        full = f"{title}\n\n{desc}"
        triggers = keyword_classify(full, TRIGGERS)
        themes   = keyword_classify(full, THEMES)

        results.append({
            "id":       bid,
            "title":    title,
            "author":   ", ".join(info.get("authors", [])),
            "synopsis": desc,
            "coverUrl": info.get("imageLinks", {}).get("thumbnail", ""),
            "triggers": triggers,
            "themes":   themes,
        })

    return results

@app.get("/summarize")
async def summarize(id: str):

    cache_file = Path(__file__).parent / "summary_cache.json"
    if cache_file.exists():
        cache = json.loads(cache_file.read_text())
    else:
        cache = {}


    if id in cache:
        return {"summary": cache[id]}


    async with httpx.AsyncClient() as http:
        r = await http.get(
            f"https://www.googleapis.com/books/v1/volumes/{id}",
            params={"key": GOOGLE_KEY}
        )
        info = r.json().get("volumeInfo", {})

    title = info.get("title", "This book")
    desc  = info.get("description", "")
    full  = f"{title}\n\n{desc}"
    top_themes = keyword_classify(full, THEMES)[:3]


    prompt = (
        "You are a best-in-class book recommender. In a single upbeat sentence, "
        f"write a teaser.  Do not mention any negative or graphic elements—focus on what readers will love. Title: {title}; Themes: {', '.join(top_themes)}."
    )
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=60,
    )
    teaser = resp.choices[0].message.content.strip()


    cache[id] = teaser
    cache_file.write_text(json.dumps(cache, indent=2))
    return {"summary": teaser}

