
import os, requests
KEYWORDS = ["earnings","revenue","guidance","forecast","analyst","upgrade","downgrade","estimate","wall street","insider","SEC","filing","sale","partnership","acquisition","merger"]

def _keyword_filter(title, description):
    text = (title or "") + " " + (description or "")
    text = text.lower()
    for k in KEYWORDS:
        if k in text:
            return True
    return False

def fetch_filtered_news_for_ticker(ticker, news_api_key):
    if not news_api_key:
        return []
    q = f"{ticker} OR {ticker} stock OR {ticker} earnings"
    url = "https://newsapi.org/v2/everything"
    params = {"q": q, "apiKey": news_api_key, "pageSize": 10, "sortBy":"publishedAt", "language":"en"}
    r = requests.get(url, params=params, timeout=8)
    r.raise_for_status()
    data = r.json().get("articles", [])
    filtered = []
    for a in data:
        title = a.get("title","")
        desc = a.get("description","")
        if _keyword_filter(title, desc):
            filtered.append({"title": title, "url": a.get("url"), "source": a.get("source",{}).get("name"), "publishedAt": a.get("publishedAt")})
    return filtered
