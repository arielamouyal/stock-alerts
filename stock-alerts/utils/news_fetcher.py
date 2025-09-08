import os, requests

def fetch_news():
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    tickers = ["ABNB","MSFT","TSLA","UBER","BKNG","NVTS","COIN","MELI",
               "AAPL","AMZN","HOOD","MAXN","MSTR","PLTR","NVDA","MARA",
               "SBUX","SMCI","SOFI"]
    url = f"https://newsapi.org/v2/everything?q={' OR '.join(tickers)}&apiKey={NEWS_API_KEY}"
    resp = requests.get(url)
    data = resp.json()
    articles = data.get("articles", [])
    return [{"title": a["title"], "description": a.get("description",""), "url": a["url"]} for a in articles]
