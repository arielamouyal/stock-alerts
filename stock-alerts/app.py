from flask import Flask, render_template
from utils.news_fetcher import fetch_news
from utils.ai_filter import is_bullish
from utils.alerts import send_sms

app = Flask(__name__)

@app.route("/")
def index():
    news_items = fetch_news()
    bullish_news = [n for n in news_items if is_bullish(n['title'] + " " + n['description'])]
    for item in bullish_news:
        send_sms(item['title'] + " - " + item['url'])
    return render_template("index.html", news=bullish_news)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
