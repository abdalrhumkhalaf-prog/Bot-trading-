import os, requests
from flask import Flask, request, jsonify

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
SECRET_TOKEN = os.environ.get("SECRET_TOKEN")  # حط قيمته في Render (اختياري للأمان)

def send_to_telegram(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        return {"ok": False, "error": "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID"}
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    r = requests.post(url, json=payload, timeout=10)
    try:
        return r.json()
    except Exception:
        return {"ok": False, "error": r.text}

app = Flask(__name__)

@app.route("/")
def home():
    return "Trading bot is running."

@app.route("/signal", methods=["POST"])
def signal():
    # تحقق اختياري برمز سري في رابط الويب هوك
    token = request.args.get("token")
    if SECRET_TOKEN and token != SECRET_TOKEN:
        return jsonify({"ok": False, "error": "invalid token"}), 401

    data = request.get_json(silent=True)
    parts = ["🚨 <b>TradingView Alert</b>"]

    if data:
        symbol = data.get("symbol") or data.get("ticker") or ""
        price = data.get("price")
        note  = data.get("message") or data.get("note") or ""
        if symbol: parts.append(f"• Symbol: <b>{symbol}</b>")
        if price is not None: parts.append(f"• Price: <b>{price}</b>")
        if note: parts.append(f"• Note: {note}")
    else:
        raw = request.data.decode("utf-8", errors="ignore") or str(request.form)
        parts.append(raw)

    text = "\n".join(parts)
    tg_resp = send_to_telegram(text)
    return jsonify({"ok": True, "forwarded": tg_resp})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
