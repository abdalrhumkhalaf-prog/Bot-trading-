import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

@app.route("/signal", methods=["POST"])
def signal():
    data = request.json
    symbol = data.get("ticker", "غير معروف")
    close_price = float(data.get("close", 0))

    # حساب الأهداف والوقف
    target1 = round(close_price * 1.01, 4)
    target2 = round(close_price * 1.02, 4)
    stop_loss = round(close_price * 0.993, 4)

    message = f"""
📊 *إشارة تداول (15 دقيقة)*

💹 الزوج: {symbol}
✅ الدخول: {close_price}

🎯 الهدف الأول: {target1}
🎯 الهدف الثاني: {target2}
⛔ وقف الخسارة: {stop_loss}
    """

    send_telegram_message(message)
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
