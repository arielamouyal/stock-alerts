from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# Your API keys
FINNHUB_API_KEY = "d23r0t9r01qv4g01t110d23r0t9r01qv4g01t11g"
NEWS_API_KEY = "8454b1b0714a4d569f39d36683dd358f"

# Preloaded watchlist
WATCHLIST = [
    "ABNB", "MSFT", "TSLA", "UBER", "BKNG", "NVTS", "COIN",
    "MELI", "AAPL", "AMZN", "HOOD", "MAXN", "MSTR", "PLTR",
    "NVDA", "MARA", "SBUX", "SMCI", "SOFI"
]

def get_stock_price(ticker):
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return {
            "price": data.get("c", "N/A"),
            "change": data.get("dp", "N/A")
        }
    return {"price": "N/A", "change": "N/A"}

def get_stock_news(ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}&pageSize=3&sortBy=publishedAt"
    r = requests.get(url)
    if r.status_code == 200:
        articles = r.json().get("articles", [])
        return [{
            "title": a["title"],
            "url": a["url"],
            "source": a["source"]["name"]
        } for a in articles]
    return []

@app.route("/", methods=["GET", "POST"])
def index():
    global WATCHLIST
    if request.method == "POST":
        new_ticker = request.form.get("ticker").upper().strip()
        if new_ticker and new_ticker not in WATCHLIST:
            WATCHLIST.append(new_ticker)
        return redirect(url_for("index"))

    stocks_data = []
    for ticker in WATCHLIST:
        price_info = get_stock_price(ticker)
        news_info = get_stock_news(ticker)
        stocks_data.append({
            "ticker": ticker,
            "price": price_info["price"],
            "change": price_info["change"],
            "news": news_info
        })

    return render_template("index.html", stocks=stocks_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
