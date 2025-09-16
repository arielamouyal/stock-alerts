
import requests
def fetch_quote(symbol, token):
    if not token:
        return {"price":"N/A","change":"N/A","change_percent":"N/A"}
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={token}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        d = r.json()
        price = d.get("c")  # current
        prev = d.get("pc") if d.get("pc") is not None else d.get("o") # previous close fallback
        change = None
        percent = None
        if price is not None and prev is not None:
            try:
                change = round(price - prev, 4)
                percent = round((change / prev) * 100, 2) if prev != 0 else 0
            except Exception:
                change = "N/A"; percent = "N/A"
        return {"price": price if price is not None else "N/A", "change": change, "change_percent": percent}
    except Exception:
        return {"price":"N/A","change":"N/A","change_percent":"N/A"}
