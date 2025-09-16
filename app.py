
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os, requests, time
from utils.news_fetcher import fetch_filtered_news_for_ticker
from utils.price_fetcher import fetch_quote

app = Flask(__name__)

# WATCHLIST persistence (simple file)
WATCHLIST_FILE = "watchlist.json"
if os.path.exists(WATCHLIST_FILE):
    import json
    with open(WATCHLIST_FILE,"r") as f:
        WATCHLIST = json.load(f)
else:
    WATCHLIST = [
        "ABNB","MSFT","TSLA","UBER","BKNG","NVTS","COIN","MELI",
        "AAPL","AMZN","HOOD","MAXN","MSTR","PLTR","NVDA","MARA",
        "SBUX","SMCI","SOFI"
    ]
    with open(WATCHLIST_FILE,"w") as f:
        json.dump(WATCHLIST,f)

FINNHUB_KEY = os.getenv("FINNHUB_API_KEY")
NEWS_KEY = os.getenv("NEWS_API_KEY")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add():
    ticker = request.form.get("ticker","").upper().strip()
    if ticker and ticker not in WATCHLIST:
        WATCHLIST.append(ticker)
        with open(WATCHLIST_FILE,"w") as f:
            import json
            json.dump(WATCHLIST,f)
    return redirect(url_for("index"))

@app.route("/remove/<ticker>", methods=["POST"])
def remove(ticker):
    ticker = ticker.upper().strip()
    global WATCHLIST
    WATCHLIST = [t for t in WATCHLIST if t!=ticker]
    with open(WATCHLIST_FILE,"w") as f:
        import json
        json.dump(WATCHLIST,f)
    return ("",204)

@app.route("/api/stocks", methods=["GET"])
def api_stocks():
    stocks = []
    for t in WATCHLIST:
        q = fetch_quote(t, FINNHUB_KEY)
        news = []
        try:
            news = fetch_filtered_news_for_ticker(t, NEWS_KEY)
        except Exception:
            news = []
        stocks.append({
            "ticker": t,
            "price": q.get("price"),
            "change": q.get("change"),
            "change_percent": q.get("change_percent"),
            "news": news
        })
    return jsonify({"stocks": stocks, "timestamp": int(time.time())})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
