
import os
import json
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "8454b1b0714a4d569f39d36683dd358f")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "d23r0t9r01qv4g01t110d23r0t9r01qv4g01t11g")

WATCHLIST_FILE = "watchlist.json"

def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return []
    with open(WATCHLIST_FILE, "r") as f:
        return json.load(f)

def save_watchlist(watchlist):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(watchlist, f)

def get_stock_price(ticker):
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return {
            "price": data.get("c", 0),
            "change": data.get("d", 0),
            "percent_change": data.get("dp", 0),
        }
    return {"price": 0, "change": 0, "percent_change": 0}

def get_stock_news(ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}&language=en&sortBy=publishedAt"
    r = requests.get(url)
    if r.status_code == 200:
        articles = r.json().get("articles", [])
        filtered = [
            a for a in articles
            if any(
                keyword in a["title"].lower()
                for keyword in ["earnings", "guidance", "forecast", "rating", "downgrade", "upgrade", "wall street"]
            )
        ]
        return filtered[:5]
    return []

@app.route("/", methods=["GET", "POST"])
def index():
    watchlist = load_watchlist()
    if request.method == "POST":
        if "add" in request.form:
            ticker = request.form["ticker"].upper()
            if ticker not in watchlist:
                watchlist.append(ticker)
                save_watchlist(watchlist)
        elif "remove" in request.form:
            ticker = request.form["remove"]
            if ticker in watchlist:
                watchlist.remove(ticker)
                save_watchlist(watchlist)
        return redirect(url_for("index"))
    stock_data = []
    for ticker in watchlist:
        price_data = get_stock_price(ticker)
        news_data = get_stock_news(ticker)
        stock_data.append({
            "ticker": ticker,
            "price": price_data["price"],
            "change": price_data["change"],
            "percent_change": price_data["percent_change"],
            "news": news_data,
        })
    return render_template("index.html", stocks=stock_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
